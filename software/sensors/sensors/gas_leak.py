"""
LUXX HAUS Gas Leak Sensor
Detects gas leaks by monitoring PPM levels.
"""

from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING, Optional

from loguru import logger

from ..core import AlertSeverity, GasType, SensorType, get_config
from .base import BaseSensor

if TYPE_CHECKING:
    from ..controllers.gas_valve import GasValveController


# Gas-specific danger thresholds (PPM)
GAS_THRESHOLDS = {
    GasType.NATURAL_GAS: {
        "warning": 50,
        "danger": 100,
        "critical": 500,
        "lel": 50000,  # Lower Explosive Limit
    },
    GasType.PROPANE: {
        "warning": 40,
        "danger": 80,
        "critical": 400,
        "lel": 21000,
    },
    GasType.CARBON_MONOXIDE: {
        "warning": 35,
        "danger": 100,
        "critical": 400,
        "lel": None,  # Not explosive, but toxic
    },
    GasType.HYDROGEN_SULFIDE: {
        "warning": 10,
        "danger": 50,
        "critical": 100,
        "lel": 40000,
    },
}


class GasLeakSensor(BaseSensor):
    """
    Gas leak detector with PPM threshold alerts.
    
    Monitors gas concentration and triggers alerts when levels
    exceed configured thresholds.
    
    Supports multiple gas types:
        - Natural Gas (Methane) - MQ-4 sensor
        - Propane - MQ-6 sensor
        - Carbon Monoxide - MQ-7 sensor
        - Hydrogen Sulfide - MQ-136 sensor
    """

    def __init__(
        self,
        sensor_id: str = "LUXX-GLD-001",
        gas_type: Optional[GasType] = None,
        threshold_ppm: Optional[float] = None,
        valve: Optional["GasValveController"] = None,
        adc_channel: int = 1,
        simulation_mode: bool = False,
    ):
        config = get_config().sensors.gas_leak
        self.gas_type = gas_type or config.gas_type
        
        # Get gas-specific thresholds
        gas_thresholds = GAS_THRESHOLDS.get(self.gas_type, GAS_THRESHOLDS[GasType.NATURAL_GAS])
        
        super().__init__(
            sensor_id=sensor_id,
            sensor_type=SensorType.GAS_LEAK,
            threshold=threshold_ppm or config.threshold_ppm,
            unit="PPM",
            sample_interval=config.sample_interval_seconds,
            simulation_mode=simulation_mode,
        )
        
        self.danger_threshold = config.danger_threshold_ppm
        self.critical_threshold = config.critical_threshold_ppm
        self.valve = valve
        self.auto_shutoff = config.auto_shutoff
        self.adc_channel = adc_channel
        
        # MQ sensor calibration values
        self.r_load = 10.0  # Load resistance in kOhm
        self.r0 = 10.0  # Sensor resistance in clean air (calibrated)
        
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
            logger.warning(
                f"Hardware libraries not available for {self.sensor_id}, "
                "falling back to simulation mode"
            )
            self.simulation_mode = True
        except Exception as e:
            logger.error(f"Failed to initialize hardware for {self.sensor_id}: {e}")
            self.simulation_mode = True

    def read_value(self) -> float:
        """
        Read gas concentration from sensor.
        
        For real hardware:
            - Reads analog voltage from MQ-series gas sensor
            - Converts to PPM using sensor-specific calibration curve
            
        For simulation:
            - Returns random values, occasionally spiking to simulate leaks
        """
        if self.simulation_mode:
            # Simulate occasional gas detection
            if random.random() < 0.03:  # 3% chance of elevated reading
                return random.uniform(40, 150)
            return random.uniform(5, 30)
        
        if self._adc is None:
            logger.error("ADC not initialized")
            return 0.0
        
        try:
            voltage = self._adc.voltage
            
            if voltage < 0.1:
                return 0.0
            
            # Calculate sensor resistance
            rs = (3.3 - voltage) / voltage * self.r_load
            ratio = rs / self.r0
            
            # Convert ratio to PPM using gas-specific curve
            ppm = self._ratio_to_ppm(ratio)
            
            return max(0, ppm)
            
        except Exception as e:
            logger.error(f"Error reading gas sensor: {e}")
            return self.last_value or 0.0

    def _ratio_to_ppm(self, ratio: float) -> float:
        """
        Convert Rs/R0 ratio to PPM using sensor calibration curves.
        
        Each MQ sensor has a different characteristic curve.
        These are approximations - actual deployment should use
        manufacturer calibration data.
        """
        if ratio <= 0:
            return 0.0
        
        # Sensor-specific curve approximations
        curves = {
            GasType.NATURAL_GAS: (-0.35, 0.5),    # MQ-4 methane curve
            GasType.PROPANE: (-0.42, 0.4),        # MQ-6 propane curve
            GasType.CARBON_MONOXIDE: (-0.77, 0.6), # MQ-7 CO curve
            GasType.HYDROGEN_SULFIDE: (-0.44, 0.3), # MQ-136 H2S curve
        }
        
        slope, intercept = curves.get(self.gas_type, curves[GasType.NATURAL_GAS])
        
        # PPM = 10^((log10(ratio) - intercept) / slope)
        try:
            log_ratio = math.log10(ratio)
            ppm = pow(10, (log_ratio - intercept) / slope)
            return ppm
        except (ValueError, ZeroDivisionError):
            return 0.0

    def check_threshold(self, value: float) -> Optional[AlertSeverity]:
        """
        Check if gas level exceeds threshold.
        
        Higher PPM = more severe alert.
        """
        if value >= self.critical_threshold:
            return AlertSeverity.CRITICAL
        elif value >= self.danger_threshold:
            return AlertSeverity.DANGER
        elif value >= self.threshold:
            return AlertSeverity.WARNING
        return None

    def get_alert_message(self, value: float, severity: AlertSeverity) -> str:
        """Generate alert message for gas detection."""
        gas_name = self.gas_type.value.replace("_", " ").title()
        excess = value - self.threshold
        
        messages = {
            AlertSeverity.WARNING: (
                f"{gas_name} detected at {value:.1f} PPM "
                f"({excess:.1f} PPM above threshold). "
                "Ventilate area and investigate source."
            ),
            AlertSeverity.DANGER: (
                f"DANGER: {gas_name} at {value:.1f} PPM! "
                "Ventilate immediately. Do not operate electrical switches. "
                "Evacuate if symptoms develop."
            ),
            AlertSeverity.CRITICAL: (
                f"CRITICAL: {gas_name} at {value:.1f} PPM! "
                "EVACUATE IMMEDIATELY! Do not use phones or electrical devices. "
                "Call 911 from outside."
            ),
        }
        
        msg = messages.get(severity, f"Gas alert: {value:.1f} PPM")
        
        if self.consecutive_alerts >= 3:
            msg += " SUSTAINED LEAK DETECTED!"
        
        # Add LEL warning if applicable
        lel = GAS_THRESHOLDS.get(self.gas_type, {}).get("lel")
        if lel and value >= lel * 0.1:  # 10% of LEL
            percent_lel = (value / lel) * 100
            msg += f" ({percent_lel:.1f}% of Lower Explosive Limit)"
        
        return msg

    async def _on_alert(self, value: float, severity: AlertSeverity) -> None:
        """Handle alert by potentially shutting off gas."""
        if severity in [AlertSeverity.DANGER, AlertSeverity.CRITICAL]:
            if self.auto_shutoff and self.valve:
                logger.critical(f"GAS AUTO-SHUTOFF triggered by {self.sensor_id}")
                await self.valve.close(triggered_by=self.sensor_id)

    def set_valve(self, valve: "GasValveController") -> None:
        """Associate a valve controller with this sensor."""
        self.valve = valve
        logger.info(f"Valve {valve.valve_id} associated with sensor {self.sensor_id}")

    def calibrate(self, clean_air_resistance: float) -> None:
        """
        Calibrate the sensor using clean air resistance.
        
        Should be done in fresh air with no gas present.
        
        Args:
            clean_air_resistance: R0 value measured in clean air
        """
        self.r0 = clean_air_resistance
        logger.info(f"Sensor {self.sensor_id} calibrated with R0={clean_air_resistance}")


# =============================================================================
# GAS-SPECIFIC SENSOR CLASSES
# =============================================================================


class MethaneGasSensor(GasLeakSensor):
    """MQ-4 based natural gas (methane) sensor."""

    def __init__(
        self,
        sensor_id: str = "LUXX-MQ4-001",
        threshold_ppm: float = 50.0,
        valve: Optional["GasValveController"] = None,
        adc_channel: int = 1,
        simulation_mode: bool = False,
    ):
        super().__init__(
            sensor_id=sensor_id,
            gas_type=GasType.NATURAL_GAS,
            threshold_ppm=threshold_ppm,
            valve=valve,
            adc_channel=adc_channel,
            simulation_mode=simulation_mode,
        )
        # MQ-4 specific calibration
        self.r0 = 10.0  # Typical R0 for MQ-4 in clean air


class PropaneGasSensor(GasLeakSensor):
    """MQ-6 based propane/LPG sensor."""

    def __init__(
        self,
        sensor_id: str = "LUXX-MQ6-001",
        threshold_ppm: float = 40.0,
        valve: Optional["GasValveController"] = None,
        adc_channel: int = 2,
        simulation_mode: bool = False,
    ):
        super().__init__(
            sensor_id=sensor_id,
            gas_type=GasType.PROPANE,
            threshold_ppm=threshold_ppm,
            valve=valve,
            adc_channel=adc_channel,
            simulation_mode=simulation_mode,
        )


class CarbonMonoxideSensor(GasLeakSensor):
    """MQ-7 based carbon monoxide sensor."""

    def __init__(
        self,
        sensor_id: str = "LUXX-MQ7-001",
        threshold_ppm: float = 35.0,
        valve: Optional["GasValveController"] = None,
        adc_channel: int = 3,
        simulation_mode: bool = False,
    ):
        super().__init__(
            sensor_id=sensor_id,
            gas_type=GasType.CARBON_MONOXIDE,
            threshold_ppm=threshold_ppm,
            valve=valve,
            adc_channel=adc_channel,
            simulation_mode=simulation_mode,
        )
        # CO sensors don't typically trigger gas valve shutoff
        self.auto_shutoff = False

    def get_alert_message(self, value: float, severity: AlertSeverity) -> str:
        """CO-specific alert messages with health guidance."""
        base_msg = super().get_alert_message(value, severity)
        
        # Add CO-specific health warnings
        if severity == AlertSeverity.WARNING:
            base_msg += " Symptoms may include headache and fatigue."
        elif severity == AlertSeverity.DANGER:
            base_msg += " Risk of CO poisoning. Symptoms: confusion, dizziness, nausea."
        elif severity == AlertSeverity.CRITICAL:
            base_msg += " Life-threatening CO levels! Loss of consciousness possible."
        
        return base_msg
