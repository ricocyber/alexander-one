"""
LUXX HAUS Base Valve Controller
Abstract base class for valve/relay controllers.
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from loguru import logger

from ..core import emit_valve_action, get_config, get_db


class BaseValveController(ABC):
    """
    Abstract base class for valve controllers.
    
    Handles common functionality for water and gas valves:
        - State tracking
        - Database logging
        - Event emission
        - Safety interlocks
    """

    def __init__(
        self,
        valve_id: str,
        valve_type: str,
        gpio_pin: int,
        normally_open: bool = True,
        activation_delay: float = 0.5,
        simulation_mode: bool = False,
    ):
        self.valve_id = valve_id
        self.valve_type = valve_type
        self.gpio_pin = gpio_pin
        self.normally_open = normally_open
        self.activation_delay = activation_delay
        self.simulation_mode = simulation_mode or get_config().system.simulation_mode
        
        # State
        self.is_open = normally_open  # Assume normal state at startup
        self.last_action: Optional[str] = None
        self.last_action_time: Optional[datetime] = None
        self.last_triggered_by: Optional[str] = None
        
        # Safety
        self.locked = False
        self.lock_reason: Optional[str] = None
        
        # Callbacks
        self._on_open_callbacks: List[Callable[[], Any]] = []
        self._on_close_callbacks: List[Callable[[], Any]] = []
        
        # Database
        self._db = get_db()
        
        # Initialize hardware
        if not self.simulation_mode:
            self._init_hardware()
        
        logger.info(
            f"Initialized {valve_type} valve {valve_id} "
            f"(GPIO={gpio_pin}, normally_open={normally_open}, "
            f"simulation={simulation_mode})"
        )

    @abstractmethod
    def _init_hardware(self) -> None:
        """Initialize GPIO hardware. Override in subclasses."""
        pass

    @abstractmethod
    def _hardware_open(self) -> None:
        """Send open signal to hardware. Override in subclasses."""
        pass

    @abstractmethod
    def _hardware_close(self) -> None:
        """Send close signal to hardware. Override in subclasses."""
        pass

    async def open(self, triggered_by: str = "manual") -> bool:
        """
        Open the valve.
        
        Args:
            triggered_by: Identifier of what triggered the action
            
        Returns:
            True if successful, False otherwise
        """
        if self.locked:
            logger.warning(
                f"Cannot open {self.valve_id}: locked ({self.lock_reason})"
            )
            return False
        
        if self.is_open:
            logger.debug(f"{self.valve_id} already open")
            return True
        
        try:
            logger.info(f"Opening {self.valve_id} (triggered by {triggered_by})")
            
            if not self.simulation_mode:
                self._hardware_open()
                await asyncio.sleep(self.activation_delay)
            
            self.is_open = True
            self.last_action = "open"
            self.last_action_time = datetime.utcnow()
            self.last_triggered_by = triggered_by
            
            # Log to database
            await self._db.log_valve_action(
                valve_id=self.valve_id,
                valve_type=self.valve_type,
                action="open",
                triggered_by=triggered_by,
                success=True,
            )
            
            # Emit event
            await emit_valve_action(self.valve_id, "open", triggered_by)
            
            # Call callbacks
            for callback in self._on_open_callbacks:
                try:
                    result = callback()
                    if asyncio.iscoroutine(result):
                        await result
                except Exception as e:
                    logger.error(f"Error in open callback: {e}")
            
            logger.info(f"✅ {self.valve_id} OPENED")
            return True
            
        except Exception as e:
            logger.error(f"Failed to open {self.valve_id}: {e}")
            await self._db.log_valve_action(
                valve_id=self.valve_id,
                valve_type=self.valve_type,
                action="open",
                triggered_by=triggered_by,
                success=False,
                error_message=str(e),
            )
            return False

    async def close(self, triggered_by: str = "manual") -> bool:
        """
        Close the valve.
        
        Args:
            triggered_by: Identifier of what triggered the action
            
        Returns:
            True if successful, False otherwise
        """
        if self.locked and triggered_by != "emergency":
            logger.warning(
                f"Cannot close {self.valve_id}: locked ({self.lock_reason})"
            )
            return False
        
        if not self.is_open:
            logger.debug(f"{self.valve_id} already closed")
            return True
        
        try:
            logger.info(f"Closing {self.valve_id} (triggered by {triggered_by})")
            
            if not self.simulation_mode:
                self._hardware_close()
                await asyncio.sleep(self.activation_delay)
            
            self.is_open = False
            self.last_action = "close"
            self.last_action_time = datetime.utcnow()
            self.last_triggered_by = triggered_by
            
            # Log to database
            await self._db.log_valve_action(
                valve_id=self.valve_id,
                valve_type=self.valve_type,
                action="close",
                triggered_by=triggered_by,
                success=True,
            )
            
            # Emit event
            await emit_valve_action(self.valve_id, "close", triggered_by)
            
            # Call callbacks
            for callback in self._on_close_callbacks:
                try:
                    result = callback()
                    if asyncio.iscoroutine(result):
                        await result
                except Exception as e:
                    logger.error(f"Error in close callback: {e}")
            
            logger.info(f"🔴 {self.valve_id} CLOSED")
            return True
            
        except Exception as e:
            logger.error(f"Failed to close {self.valve_id}: {e}")
            await self._db.log_valve_action(
                valve_id=self.valve_id,
                valve_type=self.valve_type,
                action="close",
                triggered_by=triggered_by,
                success=False,
                error_message=str(e),
            )
            return False

    async def toggle(self, triggered_by: str = "manual") -> bool:
        """Toggle valve state."""
        if self.is_open:
            return await self.close(triggered_by)
        else:
            return await self.open(triggered_by)

    def lock(self, reason: str = "Manual lock") -> None:
        """Lock the valve to prevent state changes."""
        self.locked = True
        self.lock_reason = reason
        logger.info(f"{self.valve_id} locked: {reason}")

    def unlock(self) -> None:
        """Unlock the valve."""
        self.locked = False
        self.lock_reason = None
        logger.info(f"{self.valve_id} unlocked")

    def on_open(self, callback: Callable[[], Any]) -> None:
        """Register callback for open events."""
        self._on_open_callbacks.append(callback)

    def on_close(self, callback: Callable[[], Any]) -> None:
        """Register callback for close events."""
        self._on_close_callbacks.append(callback)

    def get_status(self) -> Dict[str, Any]:
        """Get current valve status."""
        return {
            "valve_id": self.valve_id,
            "valve_type": self.valve_type,
            "is_open": self.is_open,
            "state": "OPEN" if self.is_open else "CLOSED",
            "locked": self.locked,
            "lock_reason": self.lock_reason,
            "last_action": self.last_action,
            "last_action_time": (
                self.last_action_time.isoformat() if self.last_action_time else None
            ),
            "last_triggered_by": self.last_triggered_by,
            "gpio_pin": self.gpio_pin,
            "simulation_mode": self.simulation_mode,
        }

    def cleanup(self) -> None:
        """Cleanup GPIO resources."""
        if not self.simulation_mode:
            try:
                import RPi.GPIO as GPIO
                GPIO.cleanup(self.gpio_pin)
                logger.info(f"GPIO cleanup for {self.valve_id}")
            except Exception as e:
                logger.error(f"GPIO cleanup error: {e}")
