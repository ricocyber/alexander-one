"""
LUXX HAUS Event System
Async pub/sub event system for decoupled component communication.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set
from uuid import uuid4

from loguru import logger


class EventType(str, Enum):
    """Event types for the LUXX HAUS system."""

    # Sensor events
    SENSOR_READING = "sensor.reading"
    SENSOR_ALERT = "sensor.alert"
    SENSOR_CONNECTED = "sensor.connected"
    SENSOR_DISCONNECTED = "sensor.disconnected"
    SENSOR_ERROR = "sensor.error"

    # Valve events
    VALVE_OPENED = "valve.opened"
    VALVE_CLOSED = "valve.closed"
    VALVE_ERROR = "valve.error"

    # Alert events
    ALERT_TRIGGERED = "alert.triggered"
    ALERT_ACKNOWLEDGED = "alert.acknowledged"
    ALERT_RESOLVED = "alert.resolved"
    ALERT_ESCALATED = "alert.escalated"

    # Notification events
    NOTIFICATION_SENT = "notification.sent"
    NOTIFICATION_FAILED = "notification.failed"

    # System events
    SYSTEM_STARTED = "system.started"
    SYSTEM_STOPPED = "system.stopped"
    SYSTEM_ERROR = "system.error"
    EMERGENCY_SHUTOFF = "system.emergency_shutoff"

    # API events
    API_REQUEST = "api.request"
    WEBSOCKET_CONNECTED = "websocket.connected"
    WEBSOCKET_DISCONNECTED = "websocket.disconnected"


@dataclass
class Event:
    """Represents an event in the system."""

    type: EventType
    data: Dict[str, Any]
    source: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    event_id: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "event_id": self.event_id,
            "type": self.type.value,
            "data": self.data,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
        }

    def to_json(self) -> str:
        """Convert event to JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        """Create event from dictionary."""
        return cls(
            event_id=data.get("event_id", str(uuid4())),
            type=EventType(data["type"]),
            data=data["data"],
            source=data["source"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


# Type alias for event handlers
EventHandler = Callable[[Event], Any]
AsyncEventHandler = Callable[[Event], Any]


class EventBus:
    """
    Async event bus for publishing and subscribing to events.
    
    Supports:
    - Async event handlers
    - Wildcard subscriptions (e.g., "sensor.*")
    - Event history
    - Event filtering
    """

    def __init__(self, max_history: int = 1000):
        self._subscribers: Dict[str, Set[AsyncEventHandler]] = {}
        self._wildcard_subscribers: Dict[str, Set[AsyncEventHandler]] = {}
        self._history: List[Event] = []
        self._max_history = max_history
        self._lock = asyncio.Lock()

    def subscribe(
        self,
        event_type: EventType | str,
        handler: AsyncEventHandler,
    ) -> None:
        """
        Subscribe to an event type.
        
        Args:
            event_type: Event type to subscribe to. Can use wildcards (e.g., "sensor.*")
            handler: Async function to call when event is published
        """
        event_key = event_type.value if isinstance(event_type, EventType) else event_type

        if "*" in event_key:
            # Wildcard subscription
            if event_key not in self._wildcard_subscribers:
                self._wildcard_subscribers[event_key] = set()
            self._wildcard_subscribers[event_key].add(handler)
            logger.debug(f"Subscribed to wildcard pattern: {event_key}")
        else:
            # Exact subscription
            if event_key not in self._subscribers:
                self._subscribers[event_key] = set()
            self._subscribers[event_key].add(handler)
            logger.debug(f"Subscribed to event: {event_key}")

    def unsubscribe(
        self,
        event_type: EventType | str,
        handler: AsyncEventHandler,
    ) -> None:
        """Unsubscribe from an event type."""
        event_key = event_type.value if isinstance(event_type, EventType) else event_type

        if "*" in event_key:
            if event_key in self._wildcard_subscribers:
                self._wildcard_subscribers[event_key].discard(handler)
        else:
            if event_key in self._subscribers:
                self._subscribers[event_key].discard(handler)

    async def publish(self, event: Event) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event: Event to publish
        """
        async with self._lock:
            # Store in history
            self._history.append(event)
            if len(self._history) > self._max_history:
                self._history = self._history[-self._max_history :]

        event_key = event.type.value
        handlers: List[AsyncEventHandler] = []

        # Get exact match subscribers
        if event_key in self._subscribers:
            handlers.extend(self._subscribers[event_key])

        # Get wildcard match subscribers
        for pattern, pattern_handlers in self._wildcard_subscribers.items():
            if self._matches_pattern(event_key, pattern):
                handlers.extend(pattern_handlers)

        # Call all handlers concurrently
        if handlers:
            tasks = []
            for handler in handlers:
                try:
                    result = handler(event)
                    if asyncio.iscoroutine(result):
                        tasks.append(asyncio.create_task(result))
                except Exception as e:
                    logger.error(f"Error in event handler: {e}")

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

        logger.debug(f"Published event: {event_key} to {len(handlers)} handlers")

    def _matches_pattern(self, event_key: str, pattern: str) -> bool:
        """Check if event key matches a wildcard pattern."""
        if pattern == "*":
            return True

        pattern_parts = pattern.split(".")
        key_parts = event_key.split(".")

        for i, part in enumerate(pattern_parts):
            if part == "*":
                return True
            if i >= len(key_parts) or part != key_parts[i]:
                return False

        return len(pattern_parts) == len(key_parts)

    async def emit(
        self,
        event_type: EventType,
        data: Dict[str, Any],
        source: str,
    ) -> Event:
        """
        Convenience method to create and publish an event.
        
        Args:
            event_type: Type of event
            data: Event data
            source: Source of the event
            
        Returns:
            The created event
        """
        event = Event(type=event_type, data=data, source=source)
        await self.publish(event)
        return event

    def get_history(
        self,
        event_type: Optional[EventType] = None,
        source: Optional[str] = None,
        limit: int = 100,
    ) -> List[Event]:
        """
        Get event history with optional filtering.
        
        Args:
            event_type: Filter by event type
            source: Filter by source
            limit: Maximum events to return
            
        Returns:
            List of matching events
        """
        events = self._history

        if event_type:
            events = [e for e in events if e.type == event_type]

        if source:
            events = [e for e in events if e.source == source]

        return events[-limit:]

    def clear_history(self) -> None:
        """Clear event history."""
        self._history.clear()


# Singleton event bus instance
_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """Get the global event bus instance."""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus


# =============================================================================
# CONVENIENCE DECORATORS
# =============================================================================


def on_event(event_type: EventType | str):
    """
    Decorator to register a function as an event handler.
    
    Usage:
        @on_event(EventType.SENSOR_ALERT)
        async def handle_alert(event: Event):
            print(f"Alert: {event.data}")
    """

    def decorator(func: AsyncEventHandler):
        get_event_bus().subscribe(event_type, func)
        return func

    return decorator


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


async def emit_sensor_reading(
    sensor_id: str,
    sensor_type: str,
    value: float,
    unit: str,
    is_alert: bool = False,
) -> Event:
    """Emit a sensor reading event."""
    return await get_event_bus().emit(
        EventType.SENSOR_READING,
        {
            "sensor_id": sensor_id,
            "sensor_type": sensor_type,
            "value": value,
            "unit": unit,
            "is_alert": is_alert,
        },
        source=sensor_id,
    )


async def emit_alert(
    sensor_id: str,
    sensor_type: str,
    value: float,
    threshold: float,
    severity: str,
    message: str,
) -> Event:
    """Emit an alert event."""
    return await get_event_bus().emit(
        EventType.ALERT_TRIGGERED,
        {
            "sensor_id": sensor_id,
            "sensor_type": sensor_type,
            "value": value,
            "threshold": threshold,
            "severity": severity,
            "message": message,
        },
        source=sensor_id,
    )


async def emit_valve_action(
    valve_id: str,
    action: str,
    triggered_by: str,
) -> Event:
    """Emit a valve action event."""
    event_type = EventType.VALVE_OPENED if action == "open" else EventType.VALVE_CLOSED
    return await get_event_bus().emit(
        event_type,
        {
            "valve_id": valve_id,
            "action": action,
            "triggered_by": triggered_by,
        },
        source=valve_id,
    )


async def emit_emergency_shutoff(triggered_by: str, reason: str) -> Event:
    """Emit an emergency shutoff event."""
    return await get_event_bus().emit(
        EventType.EMERGENCY_SHUTOFF,
        {
            "triggered_by": triggered_by,
            "reason": reason,
        },
        source="system",
    )
