"""
LUXX HAUS Water Valve Controller
Controls water main shutoff valve.
"""

from __future__ import annotations

from typing import Optional

from loguru import logger

from ..core import get_config
from .base import BaseValveController


class WaterValveController(BaseValveController):
    """
    Controller for water main shutoff valve.
    
    Typically controls a motorized ball valve or solenoid valve
    on the main water supply line.
    
    Supported valve types:
        - Motorized ball valve (requires polarity reversal)
        - Solenoid valve (simple on/off)
        - Servo-actuated valve
    """

    def __init__(
        self,
        valve_id: str = "LUXX-WV-001",
        gpio_pin: Optional[int] = None,
        gpio_pin_close: Optional[int] = None,  # For motorized valves
        normally_open: bool = True,
        activation_delay: float = 5.0,  # Motorized valves are slow
        simulation_mode: bool = False,
    ):
        config = get_config().valves.water
        
        super().__init__(
            valve_id=valve_id,
            valve_type="water",
            gpio_pin=gpio_pin or config.gpio_pin,
            normally_open=normally_open,
            activation_delay=activation_delay or config.activation_delay_seconds,
            simulation_mode=simulation_mode,
        )
        
        # For motorized ball valves that need separate open/close signals
        self.gpio_pin_close = gpio_pin_close
        self.is_motorized = gpio_pin_close is not None

    def _init_hardware(self) -> None:
        """Initialize GPIO for water valve control."""
        try:
            import RPi.GPIO as GPIO
            
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.gpio_pin, GPIO.OUT, initial=GPIO.LOW)
            
            if self.gpio_pin_close:
                GPIO.setup(self.gpio_pin_close, GPIO.OUT, initial=GPIO.LOW)
            
            logger.info(
                f"Water valve GPIO initialized: "
                f"open={self.gpio_pin}, close={self.gpio_pin_close}"
            )
            
        except ImportError:
            logger.warning("RPi.GPIO not available, using simulation mode")
            self.simulation_mode = True
        except Exception as e:
            logger.error(f"GPIO init failed: {e}")
            self.simulation_mode = True

    def _hardware_open(self) -> None:
        """Send open signal to valve."""
        try:
            import RPi.GPIO as GPIO
            
            if self.is_motorized:
                # Motorized ball valve: pulse the open pin
                GPIO.output(self.gpio_pin_close, GPIO.LOW)
                GPIO.output(self.gpio_pin, GPIO.HIGH)
            else:
                # Solenoid valve: set pin high to open (or low for normally-open)
                if self.normally_open:
                    GPIO.output(self.gpio_pin, GPIO.LOW)  # De-energize to open
                else:
                    GPIO.output(self.gpio_pin, GPIO.HIGH)  # Energize to open
                    
        except Exception as e:
            logger.error(f"Hardware open failed: {e}")
            raise

    def _hardware_close(self) -> None:
        """Send close signal to valve."""
        try:
            import RPi.GPIO as GPIO
            
            if self.is_motorized:
                # Motorized ball valve: pulse the close pin
                GPIO.output(self.gpio_pin, GPIO.LOW)
                GPIO.output(self.gpio_pin_close, GPIO.HIGH)
            else:
                # Solenoid valve
                if self.normally_open:
                    GPIO.output(self.gpio_pin, GPIO.HIGH)  # Energize to close
                else:
                    GPIO.output(self.gpio_pin, GPIO.LOW)  # De-energize to close
                    
        except Exception as e:
            logger.error(f"Hardware close failed: {e}")
            raise

    def stop_motor(self) -> None:
        """Stop motorized valve motor (for ball valves)."""
        if not self.is_motorized or self.simulation_mode:
            return
        
        try:
            import RPi.GPIO as GPIO
            GPIO.output(self.gpio_pin, GPIO.LOW)
            GPIO.output(self.gpio_pin_close, GPIO.LOW)
            logger.debug("Water valve motor stopped")
        except Exception as e:
            logger.error(f"Failed to stop motor: {e}")


class MotorizedBallValve(WaterValveController):
    """
    Motorized ball valve controller.
    
    Uses a dual-relay setup for polarity reversal:
        - Relay 1 (gpio_pin): Controls direction
        - Relay 2 (gpio_pin_close): Provides power
    
    Compatible with:
        - US Solid motorized ball valves
        - Bacoeng motorized valves
        - Generic 12V/24V motorized valves
    """

    def __init__(
        self,
        valve_id: str = "LUXX-MBV-001",
        gpio_pin: int = 17,
        gpio_pin_close: int = 18,
        activation_delay: float = 8.0,  # Full stroke time
        simulation_mode: bool = False,
    ):
        super().__init__(
            valve_id=valve_id,
            gpio_pin=gpio_pin,
            gpio_pin_close=gpio_pin_close,
            normally_open=True,
            activation_delay=activation_delay,
            simulation_mode=simulation_mode,
        )


class SolenoidValve(WaterValveController):
    """
    Solenoid valve controller.
    
    Simple on/off control for solenoid valves.
    Can be configured as normally-open or normally-closed.
    
    Note: Solenoid valves consume power while actuated.
    Normally-closed valves are fail-safe for water shutoff.
    """

    def __init__(
        self,
        valve_id: str = "LUXX-SOL-001",
        gpio_pin: int = 17,
        normally_open: bool = False,  # NC is fail-safe for shutoff
        activation_delay: float = 0.5,
        simulation_mode: bool = False,
    ):
        super().__init__(
            valve_id=valve_id,
            gpio_pin=gpio_pin,
            normally_open=normally_open,
            activation_delay=activation_delay,
            simulation_mode=simulation_mode,
        )
