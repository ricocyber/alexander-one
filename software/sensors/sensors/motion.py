"""
LUXX HAUS / ALEXANDER one.0 - Motion Sensor
PIR-based motion detection for occupancy monitoring.
"""

from __future__ import annotations

import asyncio
import time
from typing import Callable, Optional

from loguru import logger

from ..core import AlertSeverity, SensorType, get_config
from .base import BaseSensor


class MotionSensor(BaseSensor):
    """
    PIR (Passive Infrared) motion sensor for occupancy detection.

    Used for:
        - Stove safety: Detect if kitchen is unattended
        - Security: Detect presence in rooms
        - Energy: Occupancy-based automation

    Supported hardware:
        - HC-SR501 PIR sensor (most common)
        - HC-SR505 mini PIR
        - AM312 PIR sensor
    """

    def __init__(
        self,
        sensor_id: str = "LUXX-PIR-001",
        gpio_pin: int = 23,
        location: str = "Kitchen",
        cooldown_seconds: float = 2.0,
        simulation_mode: bool = False,
    ):
        super().__init__(
            sensor_id=sensor_id,
            sensor_type=SensorType.MOTION,
            threshold=1.0,  # Binary: 0 = no motion, 1 = motion
            unit="detected",
            sample_interval=0.5,  # Check frequently
            simulation_mode=simulation_mode,
        )

        self.gpio_pin = gpio_pin
        self.location = location
        self.cooldown_seconds = cooldown_seconds

        # Motion tracking
        self.motion_detected = False
        self.last_motion_time: Optional[float] = None
        self.motion_callbacks: list[Callable] = []

        # Statistics
        self.total_motion_events = 0

        if not self.simulation_mode:
            self._init_hardware()

        logger.info(
            f"Motion sensor initialized: {sensor_id} "
            f"location={location} pin={gpio_pin}"
        )

    def _init_hardware(self) -> None:
        """Initialize GPIO for PIR sensor."""
        try:
            import RPi.GPIO as GPIO

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

            # Set up interrupt-based detection for immediate response
            GPIO.add_event_detect(
                self.gpio_pin,
                GPIO.RISING,
                callback=self._hardware_motion_callback,
                bouncetime=int(self.cooldown_seconds * 1000)
            )

            logger.info(f"PIR GPIO initialized: pin={self.gpio_pin}")

        except ImportError:
            logger.warning("RPi.GPIO not available, using simulation mode")
            self.simulation_mode = True
        except Exception as e:
            logger.error(f"GPIO init failed: {e}")
            self.simulation_mode = True

    def _hardware_motion_callback(self, channel: int) -> None:
        """Callback triggered by hardware interrupt on motion detection."""
        self._record_motion()

    def _record_motion(self) -> None:
        """Record a motion event."""
        now = time.time()
        self.motion_detected = True
        self.last_motion_time = now
        self.total_motion_events += 1

        logger.debug(f"Motion detected at {self.location}")

        # Notify callbacks
        for callback in self.motion_callbacks:
            try:
                callback(self.sensor_id, self.location, now)
            except Exception as e:
                logger.error(f"Motion callback error: {e}")

    def read_value(self) -> float:
        """
        Read motion state.

        Returns:
            1.0 if motion detected recently, 0.0 otherwise
        """
        if self.simulation_mode:
            # Simulate occasional motion (for testing)
            import random
            if random.random() < 0.3:  # 30% chance of motion
                self._record_motion()
                return 1.0
            return 0.0

        try:
            import RPi.GPIO as GPIO
            state = GPIO.input(self.gpio_pin)

            if state == GPIO.HIGH:
                self._record_motion()
                return 1.0
            return 0.0

        except Exception as e:
            logger.error(f"Error reading motion sensor: {e}")
            return 0.0

    def check_threshold(self, value: float) -> Optional[AlertSeverity]:
        """Motion sensors don't trigger alerts directly."""
        return None

    def get_alert_message(self, value: float, severity: AlertSeverity) -> str:
        """Generate motion alert message."""
        if value > 0:
            return f"Motion detected at {self.location}"
        return f"No motion at {self.location}"

    def seconds_since_motion(self) -> Optional[float]:
        """
        Get seconds since last motion was detected.

        Returns:
            Seconds since last motion, or None if no motion ever detected
        """
        if self.last_motion_time is None:
            return None
        return time.time() - self.last_motion_time

    def is_occupied(self, timeout_seconds: float = 300.0) -> bool:
        """
        Check if area is considered occupied.

        Args:
            timeout_seconds: How long without motion before considered unoccupied

        Returns:
            True if motion detected within timeout period
        """
        since = self.seconds_since_motion()
        if since is None:
            return False
        return since < timeout_seconds

    def add_motion_callback(self, callback: Callable) -> None:
        """
        Register callback for motion events.

        Callback signature: callback(sensor_id: str, location: str, timestamp: float)
        """
        self.motion_callbacks.append(callback)
        logger.debug(f"Motion callback registered for {self.sensor_id}")

    def remove_motion_callback(self, callback: Callable) -> None:
        """Remove a motion callback."""
        if callback in self.motion_callbacks:
            self.motion_callbacks.remove(callback)

    def get_status(self) -> dict:
        """Get current motion sensor status."""
        return {
            "sensor_id": self.sensor_id,
            "location": self.location,
            "motion_detected": self.motion_detected,
            "last_motion_time": self.last_motion_time,
            "seconds_since_motion": self.seconds_since_motion(),
            "is_occupied": self.is_occupied(),
            "total_events": self.total_motion_events,
            "simulation_mode": self.simulation_mode,
        }

    def reset(self) -> None:
        """Reset motion state."""
        self.motion_detected = False
        logger.debug(f"Motion sensor {self.sensor_id} reset")


class KitchenMotionSensor(MotionSensor):
    """Motion sensor specifically configured for kitchen/stove monitoring."""

    def __init__(
        self,
        sensor_id: str = "LUXX-PIR-KITCHEN-001",
        gpio_pin: int = 23,
        simulation_mode: bool = False,
    ):
        super().__init__(
            sensor_id=sensor_id,
            gpio_pin=gpio_pin,
            location="Kitchen",
            cooldown_seconds=1.0,  # Faster response for safety
            simulation_mode=simulation_mode,
        )
