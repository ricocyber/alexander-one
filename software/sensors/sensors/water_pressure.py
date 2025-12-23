"""
LUXX HAUS Water Pressure Sensor
Detects water leaks by monitoring pressure drops.
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Optional

from loguru import logger

from ..core import AlertSeverity, SensorType, get_config
from .base import BaseSensor

if TYPE_CHECKING:
    from ..controllers.water_valve import WaterValveController


class WaterPressureSensor(BaseSensor):
    """
    Water pressure sensor for leak detection.
    
    Monitors water pressure and triggers alerts when pressure drops
    below configured thresholds, indicating a potential leak.
    
    Thresholds:
        - WARNING: pressure < threshold (e.g., < 30 PSI)
        - DANGER: pressure < threshold * 0.75 (e.g., < 22.5 PSI)
        - CRITICAL: pressure < threshold * 0.5 (e.g., < 15 PSI)
    """

    def __init__(
        self,
        sensor_id: str = "LUXX-WPS-001",
        threshold_psi: Optional[float] = None,
        valve: Optional["WaterValveController"] = None,
        adc_channel: int = 0,
        simulation_mode: bool = False,
    ):
        config = get_config().sensors.water_pressure
        
        super().__init__(
            sensor_id=sensor_id,
            sensor_type=SensorType.WATER_PRESSURE,
            threshold=threshold_psi or config.threshold_psi,
            unit="PSI",
            sample_interval=config.sample_interval_seconds,
            simulation_mode=simulation_mode,
        )
        
        self.critical_threshold = config.critical_threshold_psi
        self.valve = valve
        self.auto_shutoff = config.auto_shutoff
        self.adc_channel = adc_channel
        
        # Hardware setup (Raspberry Pi with ADC)
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
            
            # Create SPI bus
            spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
            cs = DigitalInOut(board.D5)
            
            # Create MCP3008 object
            mcp = MCP.MCP3008(spi, cs)
            
            # Create analog input channel
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
        Read water pressure from sensor.
        
        For real hardware:
            - Reads analog voltage from pressure transducer via MCP3008 ADC
            - Converts voltage to PSI based on sensor calibration
            
        For simulation:
            - Returns random values between 25-50 PSI
            - Occasionally returns low values to simulate leaks
        """
        if self.simulation_mode:
            # Simulate occasional pressure drops
            if random.random() < 0.05:  # 5% chance of low pressure
                return random.uniform(15, 28)
            return random.uniform(35, 50)
        
        if self._adc is None:
            logger.error("ADC not initialized")
            return 0.0
        
        try:
            # Read voltage from ADC (0-3.3V)
            voltage = self._adc.voltage
            
            # Convert voltage to PSI
            # Typical pressure transducer: 0.5V = 0 PSI, 4.5V = 100 PSI
            # Scaled for 3.3V reference: 0.165V = 0 PSI, 2.97V = 100 PSI
            psi = (voltage - 0.165) * (100 / 2.805)
            
            # Clamp to valid range
            return max(0, min(150, psi))
            
        except Exception as e:
            logger.error(f"Error reading pressure sensor: {e}")
            return self.last_value or 0.0

    def check_threshold(self, value: float) -> Optional[AlertSeverity]:
        """
        Check if pressure indicates a leak.
        
        Lower pressure = more severe alert (inverse of gas sensors).
        """
        if value < self.threshold * 0.5 or value < self.critical_threshold:
            return AlertSeverity.CRITICAL
        elif value < self.threshold * 0.75:
            return AlertSeverity.DANGER
        elif value < self.threshold:
            return AlertSeverity.WARNING
        return None

    def get_alert_message(self, value: float, severity: AlertSeverity) -> str:
        """Generate alert message for pressure drop."""
        drop = self.threshold - value
        
        messages = {
            AlertSeverity.WARNING: (
                f"Water pressure at {value:.1f} PSI "
                f"({drop:.1f} PSI below normal). Monitor for leaks."
            ),
            AlertSeverity.DANGER: (
                f"Water pressure dropped to {value:.1f} PSI! "
                f"Possible leak detected. Inspect plumbing immediately."
            ),
            AlertSeverity.CRITICAL: (
                f"CRITICAL: Water pressure at {value:.1f} PSI! "
                f"Major leak likely. Water shutoff recommended."
            ),
        }
        
        msg = messages.get(severity, f"Pressure alert: {value:.1f} PSI")
        
        if self.consecutive_alerts >= 3:
            msg += " SUSTAINED PRESSURE DROP - Check for burst pipe!"
        
        return msg

    async def _on_alert(self, value: float, severity: AlertSeverity) -> None:
        """Handle alert by potentially shutting off water."""
        if severity == AlertSeverity.CRITICAL and self.auto_shutoff and self.valve:
            logger.critical(f"AUTO-SHUTOFF triggered by {self.sensor_id}")
            await self.valve.close(triggered_by=self.sensor_id)

    def set_valve(self, valve: "WaterValveController") -> None:
        """Associate a valve controller with this sensor."""
        self.valve = valve
        logger.info(f"Valve {valve.valve_id} associated with sensor {self.sensor_id}")


# =============================================================================
# HARDWARE-SPECIFIC IMPLEMENTATIONS
# =============================================================================


class HoneywellPX2Sensor(WaterPressureSensor):
    """
    Honeywell PX2 Series pressure transducer.
    
    Specs:
        - Output: 0.5V to 4.5V (ratiometric)
        - Range: 0-100 PSI (PX2AG2XX100PAAAX)
        - Accuracy: ±1% FSS
    """

    def __init__(
        self,
        sensor_id: str = "LUXX-HW-PX2-001",
        threshold_psi: Optional[float] = None,
        valve: Optional["WaterValveController"] = None,
        adc_channel: int = 0,
        supply_voltage: float = 5.0,
        simulation_mode: bool = False,
    ):
        super().__init__(
            sensor_id=sensor_id,
            threshold_psi=threshold_psi,
            valve=valve,
            adc_channel=adc_channel,
            simulation_mode=simulation_mode,
        )
        self.supply_voltage = supply_voltage

    def read_value(self) -> float:
        """Read pressure using Honeywell PX2 calibration."""
        if self.simulation_mode:
            return super().read_value()
        
        if self._adc is None:
            return 0.0
        
        try:
            voltage = self._adc.voltage
            
            # PX2 output: 10% to 90% of supply voltage
            v_min = self.supply_voltage * 0.10
            v_max = self.supply_voltage * 0.90
            
            # Linear interpolation
            psi = (voltage - v_min) / (v_max - v_min) * 100
            
            return max(0, min(150, psi))
            
        except Exception as e:
            logger.error(f"Error reading Honeywell PX2: {e}")
            return self.last_value or 0.0
