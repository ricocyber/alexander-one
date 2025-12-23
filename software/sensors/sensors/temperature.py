"""
LUXX HAUS Temperature Sensor
Monitors temperature for freeze prevention and heat alerts.
"""

from __future__ import annotations

import random
from typing import Optional

from loguru import logger

from ..core import AlertSeverity, SensorType, get_config
from .base import BaseSensor


class TemperatureSensor(BaseSensor):
    """
    Temperature sensor using DHT22 or similar.
    
    Features:
        - Freeze warning (pipes may freeze)
        - High temperature alerts
        - Humidity monitoring (optional)
    """

    def __init__(
        self,
        sensor_id: str = "LUXX-TMP-001",
        freeze_threshold_f: Optional[float] = None,
        high_threshold_f: Optional[float] = None,
        location: str = "Unknown",
        gpio_pin: Optional[int] = None,
        simulation_mode: bool = False,
    ):
        config = get_config().sensors.temperature
        
        self.freeze_threshold = freeze_threshold_f or config.freeze_threshold_f
        self.high_threshold = high_threshold_f or config.high_threshold_f
        
        super().__init__(
            sensor_id=sensor_id,
            sensor_type=SensorType.TEMPERATURE,
            threshold=self.freeze_threshold,  # Primary threshold for freezing
            unit="°F",
            sample_interval=config.sample_interval_seconds,
            simulation_mode=simulation_mode,
        )
        
        self.location = location
        self.gpio_pin = gpio_pin or config.gpio_pin
        
        # Also track humidity
        self.humidity: Optional[float] = None
        
        # Hardware
        self._dht_device = None
        if not self.simulation_mode:
            self._init_hardware()

    def _init_hardware(self) -> None:
        """Initialize DHT22 sensor."""
        try:
            import board
            import adafruit_dht
            
            # Map GPIO number to board pin
            pin_map = {
                4: board.D4,
                17: board.D17,
                18: board.D18,
                27: board.D27,
                22: board.D22,
                23: board.D23,
                24: board.D24,
                25: board.D25,
            }
            
            pin = pin_map.get(self.gpio_pin, board.D4)
            self._dht_device = adafruit_dht.DHT22(pin, use_pulseio=False)
            
            logger.info(f"DHT22 initialized on GPIO {self.gpio_pin}")
            
        except ImportError:
            logger.warning("adafruit_dht not available")
            self.simulation_mode = True
        except Exception as e:
            logger.error(f"Failed to initialize DHT22: {e}")
            self.simulation_mode = True

    def read_value(self) -> float:
        """Read temperature from sensor."""
        if self.simulation_mode:
            # Simulate temperature with occasional extremes
            base_temp = 68.0 + random.uniform(-5, 5)
            
            if random.random() < 0.02:  # 2% chance of extreme
                if random.random() < 0.5:
                    return random.uniform(30, 36)  # Near freezing
                else:
                    return random.uniform(90, 100)  # High temp
            
            self.humidity = 45.0 + random.uniform(-10, 10)
            return base_temp
        
        if self._dht_device is None:
            return 0.0
        
        try:
            # DHT22 returns Celsius
            temp_c = self._dht_device.temperature
            self.humidity = self._dht_device.humidity
            
            # Convert to Fahrenheit
            temp_f = (temp_c * 9 / 5) + 32
            
            return temp_f
            
        except RuntimeError as e:
            # DHT sensors are finicky - retry is normal
            logger.debug(f"DHT read error (normal): {e}")
            return self.last_value or 68.0
        except Exception as e:
            logger.error(f"Error reading temperature: {e}")
            return self.last_value or 68.0

    def check_threshold(self, value: float) -> Optional[AlertSeverity]:
        """Check temperature thresholds."""
        # Freeze warnings (low temperature)
        if value <= 32:
            return AlertSeverity.CRITICAL
        elif value <= self.freeze_threshold:
            return AlertSeverity.DANGER
        elif value <= self.freeze_threshold + 5:
            return AlertSeverity.WARNING
        
        # High temperature warnings
        if value >= 120:
            return AlertSeverity.CRITICAL
        elif value >= self.high_threshold + 10:
            return AlertSeverity.DANGER
        elif value >= self.high_threshold:
            return AlertSeverity.WARNING
        
        return None

    def get_alert_message(self, value: float, severity: AlertSeverity) -> str:
        """Generate temperature alert message."""
        location_str = f" in {self.location}" if self.location != "Unknown" else ""
        humidity_str = f" (Humidity: {self.humidity:.0f}%)" if self.humidity else ""
        
        # Determine if this is a cold or hot alert
        is_cold = value <= self.freeze_threshold + 10
        
        if is_cold:
            messages = {
                AlertSeverity.WARNING: (
                    f"Low temperature{location_str}: {value:.1f}°F{humidity_str}. "
                    "Monitor for freezing conditions."
                ),
                AlertSeverity.DANGER: (
                    f"FREEZE WARNING{location_str}! Temperature: {value:.1f}°F{humidity_str}. "
                    "Pipes may freeze. Consider opening faucets."
                ),
                AlertSeverity.CRITICAL: (
                    f"FREEZE ALERT{location_str}! Temperature: {value:.1f}°F{humidity_str}. "
                    "PIPES AT RISK! Open faucets and apply heat immediately."
                ),
            }
        else:
            messages = {
                AlertSeverity.WARNING: (
                    f"High temperature{location_str}: {value:.1f}°F{humidity_str}. "
                    "Check HVAC system."
                ),
                AlertSeverity.DANGER: (
                    f"HEAT WARNING{location_str}! Temperature: {value:.1f}°F{humidity_str}. "
                    "Risk of heat damage. Check cooling systems."
                ),
                AlertSeverity.CRITICAL: (
                    f"EXTREME HEAT{location_str}! Temperature: {value:.1f}°F{humidity_str}. "
                    "Potential fire risk. Investigate immediately."
                ),
            }
        
        return messages.get(severity, f"Temperature alert: {value:.1f}°F")

    def get_status(self):
        """Get sensor status including humidity."""
        status = super().get_status()
        status["humidity"] = self.humidity
        status["freeze_threshold"] = self.freeze_threshold
        status["high_threshold"] = self.high_threshold
        return status


class HumiditySensor(BaseSensor):
    """
    Dedicated humidity sensor.
    
    Monitors humidity to prevent:
        - Mold growth (high humidity)
        - Static electricity (low humidity)
        - Condensation damage
    """

    def __init__(
        self,
        sensor_id: str = "LUXX-HUM-001",
        high_threshold: float = 60.0,
        low_threshold: float = 30.0,
        location: str = "Unknown",
        gpio_pin: int = 4,
        simulation_mode: bool = False,
    ):
        super().__init__(
            sensor_id=sensor_id,
            sensor_type=SensorType.HUMIDITY,
            threshold=high_threshold,
            unit="%",
            sample_interval=30.0,  # Less frequent for humidity
            simulation_mode=simulation_mode,
        )
        
        self.high_threshold = high_threshold
        self.low_threshold = low_threshold
        self.location = location
        self.gpio_pin = gpio_pin
        
        # Hardware
        self._dht_device = None
        if not self.simulation_mode:
            self._init_hardware()

    def _init_hardware(self) -> None:
        """Initialize DHT22 for humidity reading."""
        try:
            import board
            import adafruit_dht
            
            pin_map = {4: board.D4, 17: board.D17, 18: board.D18}
            pin = pin_map.get(self.gpio_pin, board.D4)
            self._dht_device = adafruit_dht.DHT22(pin, use_pulseio=False)
            
        except Exception as e:
            logger.warning(f"DHT init failed: {e}")
            self.simulation_mode = True

    def read_value(self) -> float:
        """Read humidity from sensor."""
        if self.simulation_mode:
            base = 45.0 + random.uniform(-5, 5)
            if random.random() < 0.03:
                return random.uniform(65, 80) if random.random() < 0.5 else random.uniform(15, 25)
            return base
        
        if self._dht_device is None:
            return 45.0
        
        try:
            return self._dht_device.humidity or 45.0
        except Exception as e:
            logger.debug(f"DHT humidity read error: {e}")
            return self.last_value or 45.0

    def check_threshold(self, value: float) -> Optional[AlertSeverity]:
        """Check humidity thresholds."""
        # High humidity (mold risk)
        if value >= 80:
            return AlertSeverity.DANGER
        elif value >= self.high_threshold:
            return AlertSeverity.WARNING
        
        # Low humidity
        if value <= 15:
            return AlertSeverity.DANGER
        elif value <= self.low_threshold:
            return AlertSeverity.WARNING
        
        return None

    def get_alert_message(self, value: float, severity: AlertSeverity) -> str:
        """Generate humidity alert message."""
        location_str = f" in {self.location}" if self.location != "Unknown" else ""
        
        if value >= self.high_threshold:
            return (
                f"High humidity{location_str}: {value:.0f}%. "
                f"Risk of mold growth. Consider dehumidifier."
            )
        else:
            return (
                f"Low humidity{location_str}: {value:.0f}%. "
                f"Consider humidifier to prevent dryness."
            )
