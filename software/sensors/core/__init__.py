"""
LUXX HAUS Core Module
Contains configuration, database, event system, and central monitor.
"""

from .config import (
    AlertSeverity,
    GasType,
    LuxxHausConfig,
    SensorType,
    get_config,
    load_config,
    set_config,
)
from .database import (
    Alert,
    Base,
    DatabaseManager,
    SensorReading,
    SystemEvent,
    ValveAction,
    get_db,
    init_db,
)
from .events import (
    Event,
    EventBus,
    EventType,
    emit_alert,
    emit_emergency_shutoff,
    emit_sensor_reading,
    emit_valve_action,
    get_event_bus,
    on_event,
)
from .monitor import LuxxHausMonitor, create_default_monitor, run_demo

__all__ = [
    # Config
    "AlertSeverity",
    "GasType",
    "SensorType",
    "LuxxHausConfig",
    "get_config",
    "set_config",
    "load_config",
    # Database
    "Base",
    "SensorReading",
    "Alert",
    "ValveAction",
    "SystemEvent",
    "DatabaseManager",
    "get_db",
    "init_db",
    # Events
    "Event",
    "EventType",
    "EventBus",
    "get_event_bus",
    "on_event",
    "emit_sensor_reading",
    "emit_alert",
    "emit_valve_action",
    "emit_emergency_shutoff",
    # Monitor
    "LuxxHausMonitor",
    "create_default_monitor",
    "run_demo",
]
