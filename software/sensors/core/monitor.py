"""
LUXX HAUS Central Monitoring System
Orchestrates all sensors, valves, and notifications.
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Type

from loguru import logger

from .core import (
    AlertSeverity,
    EventType,
    GasType,
    LuxxHausConfig,
    SensorType,
    emit_emergency_shutoff,
    get_config,
    get_db,
    get_event_bus,
    init_db,
    load_config,
)
from .controllers import (
    GasSolenoidValve,
    GasValveController,
    MotorizedBallValve,
    StoveSafetyController,
    WaterValveController,
)
from .notifications import NotificationManager, get_notification_manager
from .sensors import (
    BaseSensor,
    CarbonMonoxideSensor,
    GasLeakSensor,
    MotionSensor,
    SmokeSensor,
    StoveHeatSensor,
    TemperatureSensor,
    WaterPressureSensor,
)


class LuxxHausMonitor:
    """
    Central monitoring system for LUXX HAUS.
    
    Manages all sensors, valves, notifications, and system events.
    
    Usage:
        monitor = LuxxHausMonitor()
        monitor.add_water_sensor()
        monitor.add_gas_sensor()
        await monitor.start()
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        simulation_mode: bool = False,
    ):
        # Load configuration
        if config_path:
            self.config = load_config(config_path)
        else:
            self.config = get_config()
        
        # Override simulation mode if specified
        if simulation_mode:
            self.config.system.simulation_mode = True
        
        # Initialize database
        self._db = init_db()
        
        # Initialize components
        self.sensors: Dict[str, BaseSensor] = {}
        self.valves: Dict[str, Any] = {}
        self.notification_manager: Optional[NotificationManager] = None
        
        # Initialize valves
        self._init_valves()
        
        # State
        self.is_running = False
        self._monitor_tasks: Dict[str, asyncio.Task] = {}
        self._start_time: Optional[datetime] = None
        
        # Event bus
        self._event_bus = get_event_bus()
        self._setup_event_handlers()
        
        logger.info(
            f"LUXX HAUS Monitor initialized "
            f"(simulation_mode={self.config.system.simulation_mode})"
        )

    def _init_valves(self) -> None:
        """Initialize valve controllers based on configuration."""
        valve_config = self.config.valves
        simulation = self.config.system.simulation_mode
        
        # Water valve
        if valve_config.water.enabled:
            self.valves["water"] = WaterValveController(
                valve_id="LUXX-WV-MAIN",
                gpio_pin=valve_config.water.gpio_pin,
                normally_open=valve_config.water.normally_open,
                simulation_mode=simulation,
            )
        
        # Gas valve
        if valve_config.gas.enabled:
            self.valves["gas"] = GasValveController(
                valve_id="LUXX-GV-MAIN",
                gpio_pin=valve_config.gas.gpio_pin,
                simulation_mode=simulation,
            )

    def _setup_event_handlers(self) -> None:
        """Set up event bus subscriptions."""
        # Subscribe to emergency events
        self._event_bus.subscribe(
            EventType.EMERGENCY_SHUTOFF,
            self._handle_emergency_shutoff,
        )

    async def _handle_emergency_shutoff(self, event) -> None:
        """Handle emergency shutoff event."""
        logger.critical(f"Emergency shutoff triggered: {event.data}")
        await self.emergency_shutoff(
            triggered_by=event.data.get("triggered_by", "event"),
            reason=event.data.get("reason", "Unknown"),
        )

    # =========================================================================
    # SENSOR MANAGEMENT
    # =========================================================================

    def add_sensor(self, sensor: BaseSensor) -> BaseSensor:
        """Add a sensor to the monitoring system."""
        self.sensors[sensor.sensor_id] = sensor
        logger.info(f"Added sensor: {sensor.sensor_id} ({sensor.sensor_type.value})")
        return sensor

    def add_water_sensor(
        self,
        sensor_id: str = "LUXX-WPS-001",
        threshold_psi: Optional[float] = None,
        location: str = "Main Water Line",
    ) -> WaterPressureSensor:
        """Add a water pressure sensor."""
        config = self.config.sensors.water_pressure
        
        sensor = WaterPressureSensor(
            sensor_id=sensor_id,
            threshold_psi=threshold_psi or config.threshold_psi,
            valve=self.valves.get("water"),
            adc_channel=config.adc_channel,
            simulation_mode=self.config.system.simulation_mode,
        )
        
        return self.add_sensor(sensor)

    def add_gas_sensor(
        self,
        sensor_id: str = "LUXX-GLD-001",
        threshold_ppm: Optional[float] = None,
        gas_type: Optional[GasType] = None,
        location: str = "Kitchen",
    ) -> GasLeakSensor:
        """Add a gas leak sensor."""
        config = self.config.sensors.gas_leak
        
        sensor = GasLeakSensor(
            sensor_id=sensor_id,
            gas_type=gas_type or config.gas_type,
            threshold_ppm=threshold_ppm or config.threshold_ppm,
            valve=self.valves.get("gas"),
            adc_channel=config.adc_channel,
            simulation_mode=self.config.system.simulation_mode,
        )
        
        return self.add_sensor(sensor)

    def add_co_sensor(
        self,
        sensor_id: str = "LUXX-CO-001",
        threshold_ppm: float = 35.0,
        location: str = "Bedroom",
    ) -> CarbonMonoxideSensor:
        """Add a carbon monoxide sensor."""
        sensor = CarbonMonoxideSensor(
            sensor_id=sensor_id,
            threshold_ppm=threshold_ppm,
            simulation_mode=self.config.system.simulation_mode,
        )
        
        return self.add_sensor(sensor)

    def add_smoke_sensor(
        self,
        sensor_id: str = "LUXX-SMK-001",
        threshold_ppm: Optional[float] = None,
        location: str = "Hallway",
    ) -> SmokeSensor:
        """Add a smoke detector."""
        config = self.config.sensors.smoke
        
        sensor = SmokeSensor(
            sensor_id=sensor_id,
            threshold_ppm=threshold_ppm or config.threshold_ppm,
            location=location,
            adc_channel=config.adc_channel,
            simulation_mode=self.config.system.simulation_mode,
        )
        
        return self.add_sensor(sensor)

    def add_temperature_sensor(
        self,
        sensor_id: str = "LUXX-TMP-001",
        location: str = "Basement",
    ) -> TemperatureSensor:
        """Add a temperature sensor."""
        config = self.config.sensors.temperature
        
        sensor = TemperatureSensor(
            sensor_id=sensor_id,
            freeze_threshold_f=config.freeze_threshold_f,
            high_threshold_f=config.high_threshold_f,
            location=location,
            gpio_pin=config.gpio_pin,
            simulation_mode=self.config.system.simulation_mode,
        )

        return self.add_sensor(sensor)

    def add_stove_safety(
        self,
        controller_id: str = "LUXX-STOVE-SAFETY-001",
        warning_timeout_seconds: float = 180.0,
        shutoff_timeout_seconds: float = 300.0,
    ) -> StoveSafetyController:
        """
        Add stove safety controller for unattended cooking protection.

        This is ALEXANDER's unique differentiator - no competitor has this.

        Args:
            controller_id: Unique identifier for the controller
            warning_timeout_seconds: Time without motion before warning (default 3 min)
            shutoff_timeout_seconds: Time without motion before gas shutoff (default 5 min)

        Returns:
            StoveSafetyController instance
        """
        config = self.config.sensors.stove_safety

        if not config.enabled:
            logger.warning("Stove safety is disabled in configuration")
            return None

        controller = StoveSafetyController(
            controller_id=controller_id,
            gas_valve=self.valves.get("gas"),
            warning_timeout_seconds=warning_timeout_seconds or config.warning_timeout_seconds,
            shutoff_timeout_seconds=shutoff_timeout_seconds or config.unattended_timeout_seconds,
            simulation_mode=self.config.system.simulation_mode,
        )

        # Store controller
        self.valves["stove_safety"] = controller

        logger.info(
            f"Stove safety controller added: {controller_id} "
            f"(warning={warning_timeout_seconds}s, shutoff={shutoff_timeout_seconds}s)"
        )

        return controller

    def remove_sensor(self, sensor_id: str) -> bool:
        """Remove a sensor from the system."""
        if sensor_id in self.sensors:
            sensor = self.sensors[sensor_id]
            sensor.stop_monitoring()
            del self.sensors[sensor_id]
            logger.info(f"Removed sensor: {sensor_id}")
            return True
        return False

    # =========================================================================
    # VALVE CONTROL
    # =========================================================================

    async def open_water_valve(self, triggered_by: str = "manual") -> bool:
        """Open the water main valve."""
        valve = self.valves.get("water")
        if valve:
            return await valve.open(triggered_by)
        logger.warning("No water valve configured")
        return False

    async def close_water_valve(self, triggered_by: str = "manual") -> bool:
        """Close the water main valve."""
        valve = self.valves.get("water")
        if valve:
            return await valve.close(triggered_by)
        logger.warning("No water valve configured")
        return False

    async def open_gas_valve(self, triggered_by: str = "manual") -> bool:
        """Open the gas valve."""
        valve = self.valves.get("gas")
        if valve:
            return await valve.open(triggered_by)
        logger.warning("No gas valve configured")
        return False

    async def close_gas_valve(self, triggered_by: str = "manual") -> bool:
        """Close the gas valve."""
        valve = self.valves.get("gas")
        if valve:
            return await valve.close(triggered_by)
        logger.warning("No gas valve configured")
        return False

    async def emergency_shutoff(
        self,
        triggered_by: str = "manual",
        reason: str = "Emergency",
    ) -> Dict[str, bool]:
        """
        Emergency shutoff of all valves.
        
        Returns dict of valve -> success status.
        """
        logger.critical(f"🚨 EMERGENCY SHUTOFF - {reason} (by {triggered_by})")
        
        results = {}
        
        # Close all valves
        for valve_type, valve in self.valves.items():
            try:
                # Use emergency close if available
                if hasattr(valve, "emergency_close"):
                    success = await valve.emergency_close()
                else:
                    success = await valve.close(triggered_by="emergency")
                results[valve_type] = success
            except Exception as e:
                logger.error(f"Failed to close {valve_type} valve: {e}")
                results[valve_type] = False
        
        # Send critical notification
        if self.notification_manager:
            await self.notification_manager.send_alert(
                title="🚨 Emergency Shutoff Activated",
                message=f"All valves closed. Reason: {reason}. Triggered by: {triggered_by}",
                severity=AlertSeverity.CRITICAL,
            )
        
        # Emit event
        await emit_emergency_shutoff(triggered_by, reason)
        
        return results

    # =========================================================================
    # MONITORING CONTROL
    # =========================================================================

    async def start(self) -> None:
        """Start monitoring all sensors."""
        if self.is_running:
            logger.warning("Monitor already running")
            return
        
        if not self.sensors:
            logger.warning("No sensors registered. Add sensors before starting.")
            return
        
        self.is_running = True
        self._start_time = datetime.utcnow()
        
        # Initialize notification manager
        self.notification_manager = get_notification_manager()
        
        # Log system start
        await self._db.log_event(
            event_type="system_start",
            source="monitor",
            message=f"LUXX HAUS started with {len(self.sensors)} sensors",
        )
        
        # Emit start event
        await self._event_bus.emit(
            EventType.SYSTEM_STARTED,
            {"sensors": len(self.sensors), "valves": len(self.valves)},
            "monitor",
        )
        
        logger.info("=" * 60)
        logger.info("  🏠 LUXX HAUS SMART HOME PROTECTION SYSTEM")
        logger.info("=" * 60)
        logger.info(f"  Location: {self.config.system.location}")
        logger.info(f"  Sensors: {len(self.sensors)}")
        logger.info(f"  Valves: {len(self.valves)}")
        logger.info(f"  Simulation: {self.config.system.simulation_mode}")
        logger.info("=" * 60)
        
        # Start monitoring tasks for each sensor
        for sensor_id, sensor in self.sensors.items():
            task = asyncio.create_task(
                sensor.start_monitoring(),
                name=f"monitor_{sensor_id}",
            )
            self._monitor_tasks[sensor_id] = task
            logger.info(f"Started monitoring: {sensor_id}")
        
        # Wait for all tasks (or until stopped)
        try:
            await asyncio.gather(*self._monitor_tasks.values())
        except asyncio.CancelledError:
            logger.info("Monitoring tasks cancelled")

    async def stop(self) -> None:
        """Stop all monitoring."""
        if not self.is_running:
            return
        
        logger.info("Stopping LUXX HAUS monitoring...")
        self.is_running = False
        
        # Stop all sensors
        for sensor in self.sensors.values():
            sensor.stop_monitoring()
        
        # Cancel all tasks
        for task in self._monitor_tasks.values():
            task.cancel()
        
        self._monitor_tasks.clear()
        
        # Log system stop
        await self._db.log_event(
            event_type="system_stop",
            source="monitor",
            message="LUXX HAUS stopped",
        )
        
        # Emit stop event
        await self._event_bus.emit(
            EventType.SYSTEM_STOPPED,
            {},
            "monitor",
        )
        
        logger.info("LUXX HAUS monitoring stopped")

    # =========================================================================
    # STATUS & REPORTING
    # =========================================================================

    def get_status(self) -> Dict[str, Any]:
        """Get complete system status."""
        return {
            "system": {
                "name": self.config.system.name,
                "location": self.config.system.location,
                "is_running": self.is_running,
                "simulation_mode": self.config.system.simulation_mode,
                "uptime": (
                    str(datetime.utcnow() - self._start_time)
                    if self._start_time else None
                ),
            },
            "sensors": {
                sid: sensor.get_status()
                for sid, sensor in self.sensors.items()
            },
            "valves": {
                vid: valve.get_status()
                for vid, valve in self.valves.items()
            },
            "notifications": (
                self.notification_manager.get_status()
                if self.notification_manager else None
            ),
        }

    def get_sensor_readings(self) -> Dict[str, Any]:
        """Get current readings from all sensors."""
        return {
            sensor.sensor_id: {
                "value": sensor.last_value,
                "unit": sensor.unit,
                "timestamp": (
                    sensor.last_reading_time.isoformat()
                    if sensor.last_reading_time else None
                ),
                "is_alert": sensor.consecutive_alerts > 0,
            }
            for sensor in self.sensors.values()
        }

    async def get_alert_history(self, limit: int = 100) -> List[Dict]:
        """Get recent alerts from database."""
        alerts = await self._db.get_unacknowledged_alerts()
        return [
            {
                "id": a.id,
                "sensor_id": a.sensor_id,
                "severity": a.severity,
                "message": a.message,
                "timestamp": a.timestamp.isoformat(),
                "acknowledged": a.acknowledged,
            }
            for a in alerts[:limit]
        ]

    # =========================================================================
    # CONTEXT MANAGER
    # =========================================================================

    async def __aenter__(self) -> "LuxxHausMonitor":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.stop()
        
        # Cleanup valves
        for valve in self.valves.values():
            if hasattr(valve, "cleanup"):
                valve.cleanup()


# =============================================================================
# QUICK START FACTORY
# =============================================================================


def create_default_monitor(
    simulation_mode: bool = True,
) -> LuxxHausMonitor:
    """
    Create a monitor with default sensor configuration.
    
    Useful for quick testing and demos.
    """
    monitor = LuxxHausMonitor(simulation_mode=simulation_mode)
    
    # Add standard sensors
    monitor.add_water_sensor(location="Main Water Line")
    monitor.add_gas_sensor(location="Kitchen", gas_type=GasType.NATURAL_GAS)
    monitor.add_co_sensor(location="Bedroom")
    monitor.add_smoke_sensor(location="Hallway")
    monitor.add_temperature_sensor(location="Basement")
    
    return monitor


async def run_demo(duration_seconds: int = 30) -> None:
    """Run a quick demo of the system."""
    monitor = create_default_monitor(simulation_mode=True)
    
    async with monitor:
        # Start monitoring in background
        monitor_task = asyncio.create_task(monitor.start())
        
        # Run for specified duration
        await asyncio.sleep(duration_seconds)
        
        # Print status
        status = monitor.get_status()
        logger.info(f"Final status: {status}")
        
        # Stop
        await monitor.stop()
        monitor_task.cancel()
