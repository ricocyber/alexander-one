"""
LUXX HAUS / ALEXANDER one.1 - Stove Heat Sensor
Infrared temperature sensor for stove/cooktop monitoring.
"""

from __future__ import annotations

import random
import time
from typing import Optional

from loguru import logger

from ..core import AlertSeverity, SensorType, get_config
from .base import BaseSensor


class StoveHeatSensor(BaseSensor):
    """
    Infrared temperature sensor for stove/cooktop surface monitoring.

    Used for:
        - Detecting active cooking (stove is on)
        - Monitoring dangerous temperature levels
        - Integration with stove safety controller

    Supported hardware:
        - MLX90614 IR temperature sensor (I2C)
        - MLX90640 IR thermal camera
        - K-type thermocouple with MAX31855
    """

    def __init__(
        self,
        sensor_id: str = "LUXX-STOVE-HEAT-001",
        gpio_pin: int = 24,
        i2c_address: int = 0x5A,
        heat_threshold_f: float = 150.0,
        danger_threshold_f: float = 300.0,
        simulation_mode: bool = False,
    ):
        config = get_config().sensors.stove_safety

        super().__init__(
            sensor_id=sensor_id,
            sensor_type=SensorType.STOVE_HEAT,
            threshold=heat_threshold_f or config.heat_threshold_f,
            unit="°F",
            sample_interval=config.sample_interval_seconds,
            simulation_mode=simulation_mode,
        )

        self.gpio_pin = gpio_pin
        self.i2c_address = i2c_address
        self.heat_threshold_f = heat_threshold_f or config.heat_threshold_f
        self.danger_threshold_f = danger_threshold_f or config.danger_threshold_f

        # State tracking
        self.stove_active = False
        self.peak_temperature: float = 0.0
        self.active_since: Optional[float] = None

        # Hardware
        self._sensor = None
        if not self.simulation_mode:
            self._init_hardware()

        logger.info(
            f"Stove heat sensor initialized: {sensor_id} "
            f"threshold={self.heat_threshold_f}°F danger={self.danger_threshold_f}°F"
        )

    def _init_hardware(self) -> None:
        """Initialize MLX90614 IR temperature sensor."""
        try:
            import board
            import busio
            import adafruit_mlx90614

            i2c = busio.I2C(board.SCL, board.SDA)
            self._sensor = adafruit_mlx90614.MLX90614(i2c, address=self.i2c_address)

            logger.info(f"MLX90614 initialized at address 0x{self.i2c_address:02X}")

        except ImportError:
            logger.warning("adafruit_mlx90614 not available, using simulation mode")
            self.simulation_mode = True
        except Exception as e:
            logger.error(f"MLX90614 init failed: {e}")
            self.simulation_mode = True

    def read_value(self) -> float:
        """
        Read stove surface temperature.

        Returns:
            Temperature in Fahrenheit
        """
        if self.simulation_mode:
            return self._simulate_temperature()

        try:
            # Read object temperature (what the sensor is pointed at)
            temp_c = self._sensor.object_temperature
            temp_f = (temp_c * 9 / 5) + 32

            # Update state
            self._update_stove_state(temp_f)

            return temp_f

        except Exception as e:
            logger.error(f"Error reading stove heat sensor: {e}")
            return 70.0  # Room temperature fallback

    def _simulate_temperature(self) -> float:
        """Simulate stove temperature for testing."""
        # Simulate cooking cycles
        base_temp = 75.0  # Room temp

        if self.stove_active:
            # Cooking - fluctuate around 200-350°F
            base_temp = random.uniform(200.0, 350.0)
            # Small chance to cool down (stove turned off)
            if random.random() < 0.05:
                self.stove_active = False
        else:
            # Not cooking - room temp with small variation
            base_temp = random.uniform(70.0, 85.0)
            # Small chance to start cooking
            if random.random() < 0.1:
                self.stove_active = True
                self.active_since = time.time()

        temp_f = base_temp + random.uniform(-5.0, 5.0)
        self._update_stove_state(temp_f)
        return temp_f

    def _update_stove_state(self, temp_f: float) -> None:
        """Update internal stove state based on temperature."""
        was_active = self.stove_active

        # Stove is "active" if temperature exceeds threshold
        self.stove_active = temp_f >= self.heat_threshold_f

        # Track when stove became active
        if self.stove_active and not was_active:
            self.active_since = time.time()
            logger.info(f"Stove activated - temperature: {temp_f:.1f}°F")
        elif not self.stove_active and was_active:
            self.active_since = None
            logger.info(f"Stove deactivated - temperature: {temp_f:.1f}°F")

        # Track peak temperature
        if temp_f > self.peak_temperature:
            self.peak_temperature = temp_f

    def check_threshold(self, value: float) -> Optional[AlertSeverity]:
        """
        Check temperature thresholds.

        Returns severity based on temperature level.
        """
        if value >= self.danger_threshold_f:
            return AlertSeverity.DANGER
        elif value >= self.heat_threshold_f:
            return AlertSeverity.WARNING
        return None

    def get_alert_message(self, value: float, severity: AlertSeverity) -> str:
        """Generate stove temperature alert message."""
        if severity == AlertSeverity.DANGER:
            return f"DANGER: Stove temperature extremely high at {value:.0f}°F"
        elif severity == AlertSeverity.WARNING:
            return f"Stove is active - temperature at {value:.0f}°F"
        return f"Stove temperature: {value:.0f}°F"

    def is_stove_on(self) -> bool:
        """Check if stove is currently active (cooking)."""
        return self.stove_active

    def get_active_duration(self) -> Optional[float]:
        """
        Get how long the stove has been active.

        Returns:
            Seconds since stove became active, or None if not active
        """
        if not self.stove_active or self.active_since is None:
            return None
        return time.time() - self.active_since

    def reset_peak(self) -> None:
        """Reset peak temperature tracking."""
        self.peak_temperature = 0.0

    def get_status(self) -> dict:
        """Get current stove heat sensor status."""
        active_duration = self.get_active_duration()
        return {
            "sensor_id": self.sensor_id,
            "stove_active": self.stove_active,
            "current_temp_f": self.last_value,
            "heat_threshold_f": self.heat_threshold_f,
            "danger_threshold_f": self.danger_threshold_f,
            "peak_temperature_f": self.peak_temperature,
            "active_duration_seconds": active_duration,
            "active_duration_minutes": active_duration / 60 if active_duration else None,
            "simulation_mode": self.simulation_mode,
        }
