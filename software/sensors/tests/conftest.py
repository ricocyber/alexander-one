"""
Pytest configuration and fixtures for LUXX HAUS tests.
"""

import asyncio
import os
import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set environment for testing
os.environ["LUXX_HAUS_SIMULATION"] = "true"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singleton instances between tests."""
    from src.core import config, database, events
    
    # Reset config
    config._config = None
    
    # Reset database
    database._db_manager = None
    
    # Reset event bus
    events._event_bus = None
    
    yield


@pytest.fixture
def test_config():
    """Create a test configuration."""
    from src.core import LuxxHausConfig, set_config
    
    config = LuxxHausConfig()
    config.system.simulation_mode = True
    config.system.name = "Test System"
    config.database.url = "sqlite:///:memory:"
    
    set_config(config)
    return config


@pytest.fixture
def test_db(test_config):
    """Create a test database."""
    from src.core import init_db
    
    db = init_db()
    yield db


@pytest.fixture
def water_sensor():
    """Create a water pressure sensor for testing."""
    from src.sensors import WaterPressureSensor
    
    return WaterPressureSensor(
        sensor_id="TEST-WPS",
        threshold_psi=30.0,
        simulation_mode=True,
    )


@pytest.fixture
def gas_sensor():
    """Create a gas leak sensor for testing."""
    from src.sensors import GasLeakSensor
    from src.core import GasType
    
    return GasLeakSensor(
        sensor_id="TEST-GLD",
        gas_type=GasType.NATURAL_GAS,
        threshold_ppm=50.0,
        simulation_mode=True,
    )


@pytest.fixture
def water_valve():
    """Create a water valve for testing."""
    from src.controllers import WaterValveController
    
    return WaterValveController(
        valve_id="TEST-WV",
        gpio_pin=17,
        simulation_mode=True,
    )


@pytest.fixture
def gas_valve():
    """Create a gas valve for testing."""
    from src.controllers import GasValveController
    
    return GasValveController(
        valve_id="TEST-GV",
        gpio_pin=27,
        simulation_mode=True,
    )


@pytest.fixture
def monitor(test_config):
    """Create a monitor for testing."""
    from src.core.monitor import LuxxHausMonitor
    
    return LuxxHausMonitor(simulation_mode=True)
