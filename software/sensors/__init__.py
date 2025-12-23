"""
LUXX HAUS Smart Home Protection System

AI-powered smart home protection platform that prevents water damage,
gas leaks, electrical fires, and other home hazards.

Usage:
    from src import LuxxHausMonitor, create_default_monitor
    
    monitor = create_default_monitor(simulation_mode=True)
    await monitor.start()
"""

from .core import (
    AlertSeverity,
    GasType,
    LuxxHausConfig,
    SensorType,
    get_config,
    load_config,
)
from .core.monitor import LuxxHausMonitor, create_default_monitor

__version__ = "1.0.0"
__author__ = "LUXX HAUS"

__all__ = [
    # Core
    "LuxxHausConfig",
    "LuxxHausMonitor",
    "create_default_monitor",
    "get_config",
    "load_config",
    # Enums
    "AlertSeverity",
    "GasType",
    "SensorType",
]
