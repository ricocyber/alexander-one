"""
Tests for LUXX HAUS valve controllers.
"""

from unittest.mock import AsyncMock, patch

import pytest

from src.controllers import (
    GasSolenoidValve,
    GasValveController,
    MotorizedBallValve,
    SolenoidValve,
    WaterValveController,
)


class TestWaterValveController:
    """Tests for WaterValveController."""

    @pytest.fixture
    def valve(self):
        """Create a water valve in simulation mode."""
        return WaterValveController(
            valve_id="TEST-WV-001",
            gpio_pin=17,
            normally_open=True,
            simulation_mode=True,
        )

    def test_initialization(self, valve):
        """Test valve initializes correctly."""
        assert valve.valve_id == "TEST-WV-001"
        assert valve.valve_type == "water"
        assert valve.gpio_pin == 17
        assert valve.normally_open is True
        assert valve.simulation_mode is True

    def test_initial_state(self, valve):
        """Test valve starts in normally_open state."""
        assert valve.is_open is True

    @pytest.mark.asyncio
    async def test_close_valve(self, valve):
        """Test closing the valve."""
        with patch.object(valve, '_db') as mock_db:
            mock_db.log_valve_action = AsyncMock()
            
            success = await valve.close(triggered_by="test")
            
            assert success is True
            assert valve.is_open is False
            assert valve.last_action == "close"
            assert valve.last_triggered_by == "test"

    @pytest.mark.asyncio
    async def test_open_valve(self, valve):
        """Test opening the valve."""
        with patch.object(valve, '_db') as mock_db:
            mock_db.log_valve_action = AsyncMock()
            
            # First close it
            await valve.close(triggered_by="test")
            
            # Then open it
            success = await valve.open(triggered_by="test")
            
            assert success is True
            assert valve.is_open is True

    @pytest.mark.asyncio
    async def test_toggle_valve(self, valve):
        """Test toggling the valve."""
        with patch.object(valve, '_db') as mock_db:
            mock_db.log_valve_action = AsyncMock()
            
            initial_state = valve.is_open
            await valve.toggle(triggered_by="test")
            assert valve.is_open != initial_state

    @pytest.mark.asyncio
    async def test_locked_valve_cannot_close(self, valve):
        """Test that locked valve cannot be operated."""
        valve.lock("Maintenance")
        
        success = await valve.close(triggered_by="test")
        
        assert success is False
        assert valve.is_open is True  # Still open
        assert valve.locked is True

    def test_unlock_valve(self, valve):
        """Test unlocking a valve."""
        valve.lock("Maintenance")
        assert valve.locked is True
        
        valve.unlock()
        assert valve.locked is False
        assert valve.lock_reason is None

    def test_get_status(self, valve):
        """Test status reporting."""
        status = valve.get_status()
        
        assert status["valve_id"] == "TEST-WV-001"
        assert status["valve_type"] == "water"
        assert status["is_open"] is True
        assert status["state"] == "OPEN"
        assert status["locked"] is False


class TestGasValveController:
    """Tests for GasValveController."""

    @pytest.fixture
    def valve(self):
        """Create a gas valve in simulation mode."""
        return GasValveController(
            valve_id="TEST-GV-001",
            gpio_pin=27,
            simulation_mode=True,
        )

    def test_initialization(self, valve):
        """Test gas valve initializes correctly."""
        assert valve.valve_id == "TEST-GV-001"
        assert valve.valve_type == "gas"
        # Gas valves should be normally-closed
        assert valve.normally_open is False

    def test_initial_state_closed(self, valve):
        """Test gas valve starts closed (safe state)."""
        assert valve.is_open is False

    def test_normally_open_forced_to_false(self):
        """Test that normally_open is forced to False for gas valves."""
        # Try to create with normally_open=True
        valve = GasValveController(
            valve_id="TEST-GV-002",
            gpio_pin=27,
            normally_open=True,  # This should be overridden
            simulation_mode=True,
        )
        
        # Should be forced to False for safety
        assert valve.normally_open is False

    @pytest.mark.asyncio
    async def test_emergency_close(self, valve):
        """Test emergency close bypasses normal delays."""
        with patch.object(valve, '_db') as mock_db:
            mock_db.log_valve_action = AsyncMock()
            
            # Open the valve first
            await valve.open(triggered_by="test")
            assert valve.is_open is True
            
            # Emergency close
            success = await valve.emergency_close()
            
            assert success is True
            assert valve.is_open is False


class TestMotorizedBallValve:
    """Tests for MotorizedBallValve."""

    @pytest.fixture
    def valve(self):
        """Create a motorized ball valve in simulation mode."""
        return MotorizedBallValve(
            valve_id="TEST-MBV-001",
            gpio_pin=17,
            gpio_pin_close=18,
            simulation_mode=True,
        )

    def test_initialization(self, valve):
        """Test motorized valve initializes correctly."""
        assert valve.valve_id == "TEST-MBV-001"
        assert valve.gpio_pin == 17
        assert valve.gpio_pin_close == 18
        assert valve.is_motorized is True


class TestSolenoidValve:
    """Tests for SolenoidValve."""

    @pytest.fixture
    def valve(self):
        """Create a solenoid valve in simulation mode."""
        return SolenoidValve(
            valve_id="TEST-SOL-001",
            gpio_pin=17,
            normally_open=False,
            simulation_mode=True,
        )

    def test_initialization(self, valve):
        """Test solenoid valve initializes correctly."""
        assert valve.valve_id == "TEST-SOL-001"
        assert valve.normally_open is False
        assert valve.is_motorized is False


class TestGasSolenoidValve:
    """Tests for GasSolenoidValve."""

    @pytest.fixture
    def valve(self):
        """Create a gas solenoid valve in simulation mode."""
        return GasSolenoidValve(
            valve_id="TEST-GSV-001",
            gpio_pin=27,
            simulation_mode=True,
        )

    def test_initialization(self, valve):
        """Test gas solenoid initializes correctly."""
        assert valve.valve_id == "TEST-GSV-001"
        assert valve.valve_type == "gas"
        assert valve.normally_open is False  # Always NC for gas
