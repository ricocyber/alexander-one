"""
LUXX HAUS REST API
FastAPI application for the smart home protection system.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from loguru import logger

from ..core import (
    AlertSeverity,
    EventType,
    GasType,
    get_config,
    get_event_bus,
    init_db,
)
from ..core.monitor import LuxxHausMonitor, create_default_monitor


# =============================================================================
# PYDANTIC SCHEMAS
# =============================================================================


class SensorReading(BaseModel):
    """Sensor reading response."""

    sensor_id: str
    sensor_type: str
    value: float
    unit: str
    timestamp: Optional[str] = None
    is_alert: bool = False
    severity: Optional[str] = None


class SensorStatus(BaseModel):
    """Sensor status response."""

    sensor_id: str
    sensor_type: str
    is_monitoring: bool
    threshold: float
    unit: str
    last_value: Optional[float]
    consecutive_alerts: int
    average: float
    trend: str


class ValveStatus(BaseModel):
    """Valve status response."""

    valve_id: str
    valve_type: str
    is_open: bool
    state: str
    locked: bool
    last_action: Optional[str]
    last_triggered_by: Optional[str]


class AlertResponse(BaseModel):
    """Alert response."""

    id: int
    sensor_id: str
    severity: str
    message: str
    timestamp: str
    acknowledged: bool


class SystemStatus(BaseModel):
    """System status response."""

    name: str
    location: str
    is_running: bool
    simulation_mode: bool
    uptime: Optional[str]
    sensor_count: int
    valve_count: int


class ValveActionRequest(BaseModel):
    """Request to control a valve."""

    triggered_by: str = "api"


class EmergencyShutoffRequest(BaseModel):
    """Emergency shutoff request."""

    triggered_by: str = "api"
    reason: str = "Emergency shutoff via API"


class AddSensorRequest(BaseModel):
    """Request to add a new sensor."""

    sensor_type: str
    sensor_id: Optional[str] = None
    threshold: Optional[float] = None
    location: str = "Unknown"
    gas_type: Optional[str] = None


class AcknowledgeAlertRequest(BaseModel):
    """Request to acknowledge an alert."""

    acknowledged_by: str = "api"


# =============================================================================
# WEBSOCKET MANAGER
# =============================================================================


class WebSocketManager:
    """Manages WebSocket connections for real-time updates."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self._setup_event_handlers()

    def _setup_event_handlers(self):
        """Subscribe to events for broadcasting."""
        event_bus = get_event_bus()
        event_bus.subscribe("sensor.*", self._broadcast_event)
        event_bus.subscribe("valve.*", self._broadcast_event)
        event_bus.subscribe("alert.*", self._broadcast_event)

    async def _broadcast_event(self, event):
        """Broadcast event to all connected clients."""
        await self.broadcast(event.to_dict())

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, data: Dict[str, Any]):
        """Broadcast data to all connected clients."""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception:
                disconnected.append(connection)
        
        for conn in disconnected:
            self.disconnect(conn)


# =============================================================================
# APPLICATION SETUP
# =============================================================================

# Global monitor instance
monitor: Optional[LuxxHausMonitor] = None
ws_manager: Optional[WebSocketManager] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    global monitor, ws_manager
    
    # Startup
    logger.info("Starting LUXX HAUS API...")
    
    # Initialize database
    init_db()
    
    # Create monitor
    config = get_config()
    monitor = create_default_monitor(
        simulation_mode=config.system.simulation_mode
    )
    
    # Start WebSocket manager
    ws_manager = WebSocketManager()
    
    # Start monitoring in background
    monitor_task = asyncio.create_task(monitor.start())
    
    yield
    
    # Shutdown
    logger.info("Shutting down LUXX HAUS API...")
    if monitor:
        await monitor.stop()
    monitor_task.cancel()


# Create FastAPI app
app = FastAPI(
    title="LUXX HAUS API",
    description="Smart Home Protection System API",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
config = get_config()
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# API ENDPOINTS
# =============================================================================


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "name": "LUXX HAUS API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# -----------------------------------------------------------------------------
# SYSTEM ENDPOINTS
# -----------------------------------------------------------------------------


@app.get("/api/v1/status", response_model=Dict[str, Any], tags=["System"])
async def get_system_status():
    """Get complete system status."""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    return monitor.get_status()


@app.post("/api/v1/emergency/shutoff", tags=["System"])
async def emergency_shutoff(request: EmergencyShutoffRequest):
    """Trigger emergency shutoff of all valves."""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    results = await monitor.emergency_shutoff(
        triggered_by=request.triggered_by,
        reason=request.reason,
    )
    
    return {
        "success": all(results.values()),
        "results": results,
        "message": "Emergency shutoff activated",
    }


# -----------------------------------------------------------------------------
# SENSOR ENDPOINTS
# -----------------------------------------------------------------------------


@app.get("/api/v1/sensors", tags=["Sensors"])
async def list_sensors():
    """List all sensors and their current status."""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    return {
        "sensors": [
            sensor.get_status()
            for sensor in monitor.sensors.values()
        ]
    }


@app.get("/api/v1/sensors/{sensor_id}", tags=["Sensors"])
async def get_sensor(sensor_id: str):
    """Get status of a specific sensor."""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    sensor = monitor.sensors.get(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    return sensor.get_status()


@app.get("/api/v1/sensors/{sensor_id}/readings", tags=["Sensors"])
async def get_sensor_readings(sensor_id: str, limit: int = 100):
    """Get recent readings for a sensor."""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    sensor = monitor.sensors.get(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    return {
        "sensor_id": sensor_id,
        "readings": [r.to_dict() for r in sensor.readings[-limit:]],
    }


@app.post("/api/v1/sensors", tags=["Sensors"])
async def add_sensor(request: AddSensorRequest):
    """Add a new sensor to the system."""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    try:
        if request.sensor_type == "water_pressure":
            sensor = monitor.add_water_sensor(
                sensor_id=request.sensor_id or "LUXX-WPS-NEW",
                threshold_psi=request.threshold,
                location=request.location,
            )
        elif request.sensor_type == "gas_leak":
            gas_type = GasType(request.gas_type) if request.gas_type else None
            sensor = monitor.add_gas_sensor(
                sensor_id=request.sensor_id or "LUXX-GLD-NEW",
                threshold_ppm=request.threshold,
                gas_type=gas_type,
                location=request.location,
            )
        elif request.sensor_type == "smoke":
            sensor = monitor.add_smoke_sensor(
                sensor_id=request.sensor_id or "LUXX-SMK-NEW",
                threshold_ppm=request.threshold,
                location=request.location,
            )
        elif request.sensor_type == "temperature":
            sensor = monitor.add_temperature_sensor(
                sensor_id=request.sensor_id or "LUXX-TMP-NEW",
                location=request.location,
            )
        elif request.sensor_type == "carbon_monoxide":
            sensor = monitor.add_co_sensor(
                sensor_id=request.sensor_id or "LUXX-CO-NEW",
                threshold_ppm=request.threshold or 35.0,
                location=request.location,
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown sensor type: {request.sensor_type}",
            )
        
        # Start monitoring the new sensor
        asyncio.create_task(sensor.start_monitoring())
        
        return {
            "success": True,
            "sensor": sensor.get_status(),
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/v1/sensors/{sensor_id}", tags=["Sensors"])
async def remove_sensor(sensor_id: str):
    """Remove a sensor from the system."""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    success = monitor.remove_sensor(sensor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    return {"success": True, "message": f"Sensor {sensor_id} removed"}


# -----------------------------------------------------------------------------
# VALVE ENDPOINTS
# -----------------------------------------------------------------------------


@app.get("/api/v1/valves", tags=["Valves"])
async def list_valves():
    """List all valves and their status."""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    return {
        "valves": [
            valve.get_status()
            for valve in monitor.valves.values()
        ]
    }


@app.get("/api/v1/valves/{valve_type}", tags=["Valves"])
async def get_valve(valve_type: str):
    """Get status of a specific valve."""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    valve = monitor.valves.get(valve_type)
    if not valve:
        raise HTTPException(status_code=404, detail="Valve not found")
    
    return valve.get_status()


@app.post("/api/v1/valves/{valve_type}/open", tags=["Valves"])
async def open_valve(valve_type: str, request: ValveActionRequest):
    """Open a valve."""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    valve = monitor.valves.get(valve_type)
    if not valve:
        raise HTTPException(status_code=404, detail="Valve not found")
    
    success = await valve.open(triggered_by=request.triggered_by)
    
    return {
        "success": success,
        "valve": valve.get_status(),
    }


@app.post("/api/v1/valves/{valve_type}/close", tags=["Valves"])
async def close_valve(valve_type: str, request: ValveActionRequest):
    """Close a valve."""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    valve = monitor.valves.get(valve_type)
    if not valve:
        raise HTTPException(status_code=404, detail="Valve not found")
    
    success = await valve.close(triggered_by=request.triggered_by)
    
    return {
        "success": success,
        "valve": valve.get_status(),
    }


# -----------------------------------------------------------------------------
# ALERT ENDPOINTS
# -----------------------------------------------------------------------------


@app.get("/api/v1/alerts", tags=["Alerts"])
async def list_alerts(acknowledged: Optional[bool] = None, limit: int = 100):
    """List alerts."""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    alerts = await monitor.get_alert_history(limit=limit)
    
    if acknowledged is not None:
        alerts = [a for a in alerts if a["acknowledged"] == acknowledged]
    
    return {"alerts": alerts}


@app.post("/api/v1/alerts/{alert_id}/acknowledge", tags=["Alerts"])
async def acknowledge_alert(alert_id: int, request: AcknowledgeAlertRequest):
    """Acknowledge an alert."""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    db = monitor._db
    alert = await db.acknowledge_alert(alert_id, request.acknowledged_by)
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {
        "success": True,
        "alert_id": alert_id,
        "acknowledged_by": request.acknowledged_by,
    }


# -----------------------------------------------------------------------------
# WEBSOCKET ENDPOINT
# -----------------------------------------------------------------------------


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    if not ws_manager:
        await websocket.close(code=1011)
        return
    
    await ws_manager.connect(websocket)
    
    try:
        while True:
            # Keep connection alive and receive any messages
            data = await websocket.receive_text()
            
            # Handle ping/pong
            if data == "ping":
                await websocket.send_text("pong")
            
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


# =============================================================================
# RUN SERVER
# =============================================================================


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """Run the API server."""
    import uvicorn
    
    config = get_config()
    uvicorn.run(
        app,
        host=config.api.host or host,
        port=config.api.port or port,
        log_level="info",
    )


if __name__ == "__main__":
    run_server()
