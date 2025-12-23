"""
LUXX HAUS Gas Valve Controller
Controls gas line shutoff valve.
"""

from __future__ import annotations

from typing import Optional

from loguru import logger

from ..core import get_config
from .base import BaseValveController


class GasValveController(BaseValveController):
    """
    Controller for gas line shutoff valve.
    
    SAFETY NOTES:
        - Gas valves should be normally-closed (fail-safe)
        - Only use valves rated for natural gas/propane
        - Ensure proper venting after shutoff
        - Professional installation required
    
    Supported valve types:
        - Gas-rated solenoid valves (CSA certified)
        - Motorized gas ball valves
    """

    def __init__(
        self,
        valve_id: str = "LUXX-GV-001",
        gpio_pin: Optional[int] = None,
        normally_open: bool = False,  # MUST be NC for safety
        activation_delay: float = 1.0,
        simulation_mode: bool = False,
    ):
        config = get_config().valves.gas
        
        # Safety check: Gas valves should be normally-closed
        if normally_open:
            logger.warning(
                "Gas valve configured as normally-open. "
                "This is NOT recommended for safety. "
                "Forcing normally-closed configuration."
            )
            normally_open = False
        
        super().__init__(
            valve_id=valve_id,
            valve_type="gas",
            gpio_pin=gpio_pin or config.gpio_pin,
            normally_open=normally_open,
            activation_delay=activation_delay or config.activation_delay_seconds,
            simulation_mode=simulation_mode,
        )
        
        # Gas valves start closed by default
        self.is_open = False

    def _init_hardware(self) -> None:
        """Initialize GPIO for gas valve control."""
        try:
            import RPi.GPIO as GPIO
            
            GPIO.setmode(GPIO.BCM)
            # Start with valve closed (de-energized for NC valve)
            GPIO.setup(self.gpio_pin, GPIO.OUT, initial=GPIO.LOW)
            
            logger.info(f"Gas valve GPIO initialized: pin={self.gpio_pin}")
            
        except ImportError:
            logger.warning("RPi.GPIO not available, using simulation mode")
            self.simulation_mode = True
        except Exception as e:
            logger.error(f"GPIO init failed: {e}")
            self.simulation_mode = True

    def _hardware_open(self) -> None:
        """Send open signal to valve (energize NC valve)."""
        try:
            import RPi.GPIO as GPIO
            GPIO.output(self.gpio_pin, GPIO.HIGH)
        except Exception as e:
            logger.error(f"Hardware open failed: {e}")
            raise

    def _hardware_close(self) -> None:
        """Send close signal to valve (de-energize NC valve)."""
        try:
            import RPi.GPIO as GPIO
            GPIO.output(self.gpio_pin, GPIO.LOW)
        except Exception as e:
            logger.error(f"Hardware close failed: {e}")
            raise

    async def emergency_close(self) -> bool:
        """
        Emergency shutoff - bypasses locks and delays.
        
        Returns:
            True if successful
        """
        logger.critical(f"EMERGENCY GAS SHUTOFF: {self.valve_id}")
        
        # Bypass normal delay for emergency
        original_delay = self.activation_delay
        self.activation_delay = 0.1
        
        # Bypass lock
        was_locked = self.locked
        self.locked = False
        
        try:
            result = await self.close(triggered_by="emergency")
            return result
        finally:
            # Restore settings
            self.activation_delay = original_delay
            if was_locked:
                self.locked = True


class GasSolenoidValve(GasValveController):
    """
    Gas-rated solenoid valve.
    
    Requirements:
        - Must be CSA/UL certified for gas
        - Typically 12V or 24V DC
        - Normally-closed for fail-safe operation
    
    Common models:
        - Emerson ASCO gas shutoff valves
        - Honeywell gas valves
    """

    def __init__(
        self,
        valve_id: str = "LUXX-GSV-001",
        gpio_pin: int = 27,
        activation_delay: float = 0.5,
        simulation_mode: bool = False,
    ):
        super().__init__(
            valve_id=valve_id,
            gpio_pin=gpio_pin,
            normally_open=False,
            activation_delay=activation_delay,
            simulation_mode=simulation_mode,
        )


class MotorizedGasBallValve(GasValveController):
    """
    Motorized gas ball valve.
    
    Slower but more reliable for main gas shutoff.
    Requires proper gas-rated ball valve with motorized actuator.
    """

    def __init__(
        self,
        valve_id: str = "LUXX-MGBV-001",
        gpio_pin: int = 27,
        gpio_pin_direction: int = 22,  # For direction control
        activation_delay: float = 5.0,  # Full stroke time
        simulation_mode: bool = False,
    ):
        super().__init__(
            valve_id=valve_id,
            gpio_pin=gpio_pin,
            activation_delay=activation_delay,
            simulation_mode=simulation_mode,
        )
        
        self.gpio_pin_direction = gpio_pin_direction
        
        if not self.simulation_mode:
            self._init_direction_pin()

    def _init_direction_pin(self) -> None:
        """Initialize direction control pin."""
        try:
            import RPi.GPIO as GPIO
            GPIO.setup(self.gpio_pin_direction, GPIO.OUT, initial=GPIO.LOW)
        except Exception as e:
            logger.error(f"Direction pin init failed: {e}")

    def _hardware_open(self) -> None:
        """Open motorized ball valve."""
        try:
            import RPi.GPIO as GPIO
            # Set direction to open
            GPIO.output(self.gpio_pin_direction, GPIO.HIGH)
            # Power motor
            GPIO.output(self.gpio_pin, GPIO.HIGH)
        except Exception as e:
            logger.error(f"Hardware open failed: {e}")
            raise

    def _hardware_close(self) -> None:
        """Close motorized ball valve."""
        try:
            import RPi.GPIO as GPIO
            # Set direction to close
            GPIO.output(self.gpio_pin_direction, GPIO.LOW)
            # Power motor
            GPIO.output(self.gpio_pin, GPIO.HIGH)
        except Exception as e:
            logger.error(f"Hardware close failed: {e}")
            raise

    def stop_motor(self) -> None:
        """Stop the motor after actuation."""
        if self.simulation_mode:
            return
        try:
            import RPi.GPIO as GPIO
            GPIO.output(self.gpio_pin, GPIO.LOW)
        except Exception as e:
            logger.error(f"Motor stop failed: {e}")
