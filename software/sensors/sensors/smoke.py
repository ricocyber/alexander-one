"""
LUXX HAUS Smoke Sensor
Detects smoke for early fire warning.
"""

from __future__ import annotations

import random
from typing import Optional

from loguru import logger

from ..core import AlertSeverity, SensorType, get_config
from .base import BaseSensor


class SmokeSensor(BaseSensor):
    """
    Smoke detector using MQ-2 or similar gas sensor.
    
    MQ-2 is sensitive to:
        - Smoke
        - LPG
        - Propane
        - Hydrogen
        - Methane
        - Alcohol
    
    For smoke detection, we focus on the particulate matter
    that creates resistance changes in the sensor.
    """

    def __init__(
        self,
        sensor_id: str = "LUXX-SMK-001",
        threshold_ppm: Optional[float] = None,
        location: str = "Unknown",
        adc_channel: int = 2,
        simulation_mode: bool = False,
    ):
        config = get_config().sensors.smoke
        
        super().__init__(
            sensor_id=sensor_id,
            sensor_type=SensorType.SMOKE,
            threshold=threshold_ppm or config.threshold_ppm,
            unit="PPM",
            sample_interval=config.sample_interval_seconds,
            simulation_mode=simulation_mode,
        )
        
        self.location = location
        self.adc_channel = adc_channel
        
        # Calibration
        self.r_load = 10.0
        self.r0 = 9.83  # MQ-2 typical clean air resistance
        
        # Hardware
        self._adc = None
        if not self.simulation_mode:
            self._init_hardware()

    def _init_hardware(self) -> None:
        """Initialize hardware interfaces."""
        try:
            import board
            import busio
            import adafruit_mcp3xxx.mcp3008 as MCP
            from adafruit_mcp3xxx.analog_in import AnalogIn
            from digitalio import DigitalInOut
            
            spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
            cs = DigitalInOut(board.D5)
            mcp = MCP.MCP3008(spi, cs)
            self._adc = AnalogIn(mcp, getattr(MCP, f"P{self.adc_channel}"))
            
            logger.info(f"Hardware initialized for {self.sensor_id}")
            
        except ImportError:
            logger.warning(f"Hardware not available for {self.sensor_id}")
            self.simulation_mode = True
        except Exception as e:
            logger.error(f"Failed to initialize hardware: {e}")
            self.simulation_mode = True

    def read_value(self) -> float:
        """Read smoke level from sensor."""
        if self.simulation_mode:
            # Simulate occasional smoke detection
            if random.random() < 0.02:  # 2% chance
                return random.uniform(15, 50)
            return random.uniform(0, 8)
        
        if self._adc is None:
            return 0.0
        
        try:
            voltage = self._adc.voltage
            
            if voltage < 0.1:
                return 0.0
            
            # Calculate sensor resistance
            rs = (3.3 - voltage) / voltage * self.r_load
            ratio = rs / self.r0
            
            # MQ-2 smoke curve approximation
            # PPM = 10^((log10(ratio) - 0.6) / -0.47)
            import math
            if ratio <= 0:
                return 0.0
            
            log_ratio = math.log10(ratio)
            ppm = pow(10, (log_ratio - 0.6) / -0.47)
            
            return max(0, ppm)
            
        except Exception as e:
            logger.error(f"Error reading smoke sensor: {e}")
            return self.last_value or 0.0

    def check_threshold(self, value: float) -> Optional[AlertSeverity]:
        """Check if smoke level indicates danger."""
        if value >= self.threshold * 5:
            return AlertSeverity.CRITICAL
        elif value >= self.threshold * 2:
            return AlertSeverity.DANGER
        elif value >= self.threshold:
            return AlertSeverity.WARNING
        return None

    def get_alert_message(self, value: float, severity: AlertSeverity) -> str:
        """Generate smoke alert message."""
        location_str = f" in {self.location}" if self.location != "Unknown" else ""
        
        messages = {
            AlertSeverity.WARNING: (
                f"Smoke detected{location_str} ({value:.1f} PPM). "
                "Check for burning food or other sources."
            ),
            AlertSeverity.DANGER: (
                f"SMOKE ALARM{location_str}! Level: {value:.1f} PPM. "
                "Investigate immediately. Prepare to evacuate."
            ),
            AlertSeverity.CRITICAL: (
                f"🔥 FIRE ALERT{location_str}! Smoke level: {value:.1f} PPM. "
                "EVACUATE NOW! Call 911!"
            ),
        }
        
        msg = messages.get(severity, f"Smoke alert: {value:.1f} PPM")
        
        if self.consecutive_alerts >= 5:
            msg += " SUSTAINED SMOKE - FIRE LIKELY!"
        
        return msg

    async def _on_alert(self, value: float, severity: AlertSeverity) -> None:
        """Handle smoke alert - trigger alarm systems."""
        if severity == AlertSeverity.CRITICAL:
            logger.critical(f"FIRE ALERT from {self.sensor_id} at {self.location}")
            # Could trigger:
            # - Audible alarm
            # - Strobe lights
            # - HVAC shutdown
            # - Emergency services notification


class PhotoelectricSmokeSensor(BaseSensor):
    """
    Photoelectric smoke detector.
    
    Uses light scattering principle - better for smoldering fires.
    Typically uses a dedicated photoelectric smoke sensor module.
    """

    def __init__(
        self,
        sensor_id: str = "LUXX-PHOTO-001",
        threshold_obscuration: float = 2.0,  # % per foot
        location: str = "Unknown",
        gpio_pin: int = 18,
        simulation_mode: bool = False,
    ):
        super().__init__(
            sensor_id=sensor_id,
            sensor_type=SensorType.SMOKE,
            threshold=threshold_obscuration,
            unit="%/ft",
            sample_interval=1.0,
            simulation_mode=simulation_mode,
        )
        
        self.location = location
        self.gpio_pin = gpio_pin
        
        if not self.simulation_mode:
            self._init_hardware()

    def _init_hardware(self) -> None:
        """Initialize GPIO for digital smoke sensor."""
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.gpio_pin, GPIO.IN)
            logger.info(f"GPIO initialized for {self.sensor_id}")
        except ImportError:
            logger.warning("RPi.GPIO not available")
            self.simulation_mode = True
        except Exception as e:
            logger.error(f"GPIO init failed: {e}")
            self.simulation_mode = True

    def read_value(self) -> float:
        """Read smoke obscuration value."""
        if self.simulation_mode:
            if random.random() < 0.02:
                return random.uniform(2.5, 8.0)
            return random.uniform(0, 1.5)
        
        try:
            import RPi.GPIO as GPIO
            
            # For digital sensors, we might use PWM duty cycle
            # or analog reading depending on sensor type
            state = GPIO.input(self.gpio_pin)
            
            # Simple digital: 1 = smoke detected
            return 10.0 if state else 0.0
            
        except Exception as e:
            logger.error(f"Error reading smoke sensor: {e}")
            return 0.0

    def check_threshold(self, value: float) -> Optional[AlertSeverity]:
        """Check obscuration threshold."""
        if value >= self.threshold * 4:
            return AlertSeverity.CRITICAL
        elif value >= self.threshold * 2:
            return AlertSeverity.DANGER
        elif value >= self.threshold:
            return AlertSeverity.WARNING
        return None

    def get_alert_message(self, value: float, severity: AlertSeverity) -> str:
        """Generate alert message."""
        location_str = f" in {self.location}" if self.location != "Unknown" else ""
        
        if severity == AlertSeverity.CRITICAL:
            return f"🔥 FIRE DETECTED{location_str}! EVACUATE IMMEDIATELY!"
        elif severity == AlertSeverity.DANGER:
            return f"SMOKE ALARM{location_str}! Investigate and prepare to evacuate."
        else:
            return f"Smoke detected{location_str}. Check for source."
