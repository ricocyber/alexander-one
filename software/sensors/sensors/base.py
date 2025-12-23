"""
LUXX HAUS Base Sensor
Abstract base class for all sensors in the system.
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from loguru import logger

from ..core import (
    AlertSeverity,
    SensorType,
    emit_alert,
    emit_sensor_reading,
    get_config,
    get_db,
)


@dataclass
class Reading:
    """Represents a single sensor reading."""

    sensor_id: str
    sensor_type: SensorType
    value: float
    unit: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    is_alert: bool = False
    severity: Optional[AlertSeverity] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sensor_id": self.sensor_id,
            "sensor_type": self.sensor_type.value,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp.isoformat(),
            "is_alert": self.is_alert,
            "severity": self.severity.value if self.severity else None,
        }


class BaseSensor(ABC):
    """
    Abstract base class for all LUXX HAUS sensors.
    
    Subclasses must implement:
        - read_value(): Read from hardware
        - check_threshold(): Determine if alert should be triggered
        - get_alert_message(): Generate alert message
    """

    def __init__(
        self,
        sensor_id: str,
        sensor_type: SensorType,
        threshold: float,
        unit: str,
        sample_interval: float = 2.0,
        simulation_mode: bool = False,
    ):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.threshold = threshold
        self.unit = unit
        self.sample_interval = sample_interval
        self.simulation_mode = simulation_mode or get_config().system.simulation_mode

        # State
        self.readings: List[Reading] = []
        self.is_monitoring = False
        self.consecutive_alerts = 0
        self.last_value: Optional[float] = None
        self.last_reading_time: Optional[datetime] = None

        # Callbacks
        self._on_alert_callbacks: List[Callable[[Reading], Any]] = []
        self._on_reading_callbacks: List[Callable[[Reading], Any]] = []

        # Database
        self._db = get_db()

        logger.info(
            f"Initialized sensor {sensor_id} "
            f"(type={sensor_type.value}, threshold={threshold} {unit}, "
            f"simulation={simulation_mode})"
        )

    # =========================================================================
    # ABSTRACT METHODS - Must be implemented by subclasses
    # =========================================================================

    @abstractmethod
    def read_value(self) -> float:
        """
        Read current value from the sensor hardware.
        
        For simulation mode, return a simulated value.
        For real hardware, implement the actual sensor reading logic.
        
        Returns:
            float: Current sensor value
        """
        pass

    @abstractmethod
    def check_threshold(self, value: float) -> Optional[AlertSeverity]:
        """
        Check if the value exceeds threshold and determine severity.
        
        Args:
            value: Current sensor reading
            
        Returns:
            AlertSeverity if threshold exceeded, None otherwise
        """
        pass

    @abstractmethod
    def get_alert_message(self, value: float, severity: AlertSeverity) -> str:
        """
        Generate a human-readable alert message.
        
        Args:
            value: Current sensor reading
            severity: Alert severity level
            
        Returns:
            Alert message string
        """
        pass

    # =========================================================================
    # CORE METHODS
    # =========================================================================

    async def take_reading(self) -> Reading:
        """
        Take a single sensor reading and process it.
        
        Returns:
            Reading object with current sensor data
        """
        # Read value from hardware/simulation
        value = self.read_value()
        self.last_value = value
        self.last_reading_time = datetime.utcnow()

        # Check threshold
        severity = self.check_threshold(value)
        is_alert = severity is not None

        # Create reading object
        reading = Reading(
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type,
            value=value,
            unit=self.unit,
            is_alert=is_alert,
            severity=severity,
        )

        # Store reading
        self.readings.append(reading)
        if len(self.readings) > 100:
            self.readings = self.readings[-100:]

        # Update consecutive alerts counter
        if is_alert:
            self.consecutive_alerts += 1
        else:
            self.consecutive_alerts = 0

        # Log to database
        await self._db.log_reading(
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type,
            value=value,
            unit=self.unit,
            is_alert=is_alert,
            severity=severity,
        )

        # Emit event
        await emit_sensor_reading(
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type.value,
            value=value,
            unit=self.unit,
            is_alert=is_alert,
        )

        # Handle alert
        if is_alert:
            await self._handle_alert(reading, severity)

        # Call callbacks
        for callback in self._on_reading_callbacks:
            try:
                result = callback(reading)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                logger.error(f"Error in reading callback: {e}")

        return reading

    async def _handle_alert(self, reading: Reading, severity: AlertSeverity) -> None:
        """Handle an alert condition."""
        message = self.get_alert_message(reading.value, severity)

        logger.warning(
            f"ALERT [{self.sensor_id}]: {severity.value.upper()} - "
            f"{reading.value:.1f} {self.unit} - {message}"
        )

        # Log alert to database
        await self._db.log_alert(
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type,
            value=reading.value,
            threshold=self.threshold,
            severity=severity,
            message=message,
        )

        # Emit alert event
        await emit_alert(
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type.value,
            value=reading.value,
            threshold=self.threshold,
            severity=severity.value,
            message=message,
        )

        # Call alert-specific action
        await self._on_alert(reading.value, severity)

        # Call alert callbacks
        for callback in self._on_alert_callbacks:
            try:
                result = callback(reading)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                logger.error(f"Error in alert callback: {e}")

    async def _on_alert(self, value: float, severity: AlertSeverity) -> None:
        """
        Override in subclasses to perform sensor-specific alert actions.
        For example, triggering automatic valve shutoff.
        """
        pass

    # =========================================================================
    # MONITORING
    # =========================================================================

    async def start_monitoring(self) -> None:
        """Start continuous monitoring loop."""
        self.is_monitoring = True
        logger.info(f"Starting monitoring for sensor {self.sensor_id}")

        while self.is_monitoring:
            try:
                reading = await self.take_reading()

                status = "OK"
                if reading.is_alert:
                    status = f"ALERT ({reading.severity.value})"

                logger.debug(
                    f"[{self.sensor_id}] {reading.value:.1f} {self.unit} [{status}]"
                )

            except Exception as e:
                logger.error(f"Error reading sensor {self.sensor_id}: {e}")

            await asyncio.sleep(self.sample_interval)

    def stop_monitoring(self) -> None:
        """Stop the monitoring loop."""
        self.is_monitoring = False
        logger.info(f"Stopped monitoring for sensor {self.sensor_id}")

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def get_average(self, last_n: int = 10) -> float:
        """Get average value from recent readings."""
        if not self.readings:
            return 0.0
        recent = self.readings[-last_n:]
        return sum(r.value for r in recent) / len(recent)

    def get_min(self, last_n: int = 10) -> float:
        """Get minimum value from recent readings."""
        if not self.readings:
            return 0.0
        recent = self.readings[-last_n:]
        return min(r.value for r in recent)

    def get_max(self, last_n: int = 10) -> float:
        """Get maximum value from recent readings."""
        if not self.readings:
            return 0.0
        recent = self.readings[-last_n:]
        return max(r.value for r in recent)

    def get_trend(self, last_n: int = 10) -> str:
        """Determine trend direction from recent readings."""
        if len(self.readings) < 2:
            return "stable"

        recent = self.readings[-last_n:]
        first_half = recent[: len(recent) // 2]
        second_half = recent[len(recent) // 2 :]

        first_avg = sum(r.value for r in first_half) / len(first_half)
        second_avg = sum(r.value for r in second_half) / len(second_half)

        diff_percent = ((second_avg - first_avg) / first_avg) * 100 if first_avg else 0

        if diff_percent > 5:
            return "rising"
        elif diff_percent < -5:
            return "falling"
        return "stable"

    # =========================================================================
    # CALLBACKS
    # =========================================================================

    def on_alert(self, callback: Callable[[Reading], Any]) -> None:
        """Register a callback for alert events."""
        self._on_alert_callbacks.append(callback)

    def on_reading(self, callback: Callable[[Reading], Any]) -> None:
        """Register a callback for all readings."""
        self._on_reading_callbacks.append(callback)

    # =========================================================================
    # STATUS
    # =========================================================================

    def get_status(self) -> Dict[str, Any]:
        """Get current sensor status."""
        return {
            "sensor_id": self.sensor_id,
            "sensor_type": self.sensor_type.value,
            "is_monitoring": self.is_monitoring,
            "simulation_mode": self.simulation_mode,
            "threshold": self.threshold,
            "unit": self.unit,
            "last_value": self.last_value,
            "last_reading_time": (
                self.last_reading_time.isoformat() if self.last_reading_time else None
            ),
            "consecutive_alerts": self.consecutive_alerts,
            "average": self.get_average(),
            "trend": self.get_trend(),
        }
