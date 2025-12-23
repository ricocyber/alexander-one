"""
Tests for LUXX HAUS sensors.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.core import AlertSeverity, GasType, SensorType
from src.sensors import (
    GasLeakSensor,
    SmokeSensor,
    TemperatureSensor,
    WaterPressureSensor,
)


class TestWaterPressureSensor:
    """Tests for WaterPressureSensor."""

    @pytest.fixture
    def sensor(self):
        """Create a sensor in simulation mode."""
        return WaterPressureSensor(
            sensor_id="TEST-WPS-001",
            threshold_psi=30.0,
            simulation_mode=True,
        )

    def test_initialization(self, sensor):
        """Test sensor initializes correctly."""
        assert sensor.sensor_id == "TEST-WPS-001"
        assert sensor.sensor_type == SensorType.WATER_PRESSURE
        assert sensor.threshold == 30.0
        assert sensor.unit == "PSI"
        assert sensor.simulation_mode is True

    def test_read_value_simulation(self, sensor):
        """Test reading values in simulation mode."""
        value = sensor.read_value()
        assert isinstance(value, float)
        assert 0 <= value <= 150  # Within reasonable range

    def test_check_threshold_normal(self, sensor):
        """Test threshold check with normal pressure."""
        severity = sensor.check_threshold(45.0)
        assert severity is None

    def test_check_threshold_warning(self, sensor):
        """Test threshold check with low pressure (warning)."""
        severity = sensor.check_threshold(28.0)
        assert severity == AlertSeverity.WARNING

    def test_check_threshold_danger(self, sensor):
        """Test threshold check with very low pressure (danger)."""
        severity = sensor.check_threshold(20.0)
        assert severity == AlertSeverity.DANGER

    def test_check_threshold_critical(self, sensor):
        """Test threshold check with critical pressure."""
        severity = sensor.check_threshold(10.0)
        assert severity == AlertSeverity.CRITICAL

    def test_get_alert_message(self, sensor):
        """Test alert message generation."""
        message = sensor.get_alert_message(25.0, AlertSeverity.WARNING)
        assert "25.0 PSI" in message
        assert "below" in message.lower()

    @pytest.mark.asyncio
    async def test_take_reading(self, sensor):
        """Test taking a reading."""
        with patch.object(sensor, '_db') as mock_db:
            mock_db.log_reading = AsyncMock()
            
            reading = await sensor.take_reading()
            
            assert reading.sensor_id == "TEST-WPS-001"
            assert reading.sensor_type == SensorType.WATER_PRESSURE
            assert reading.unit == "PSI"

    def test_get_status(self, sensor):
        """Test status reporting."""
        status = sensor.get_status()
        
        assert status["sensor_id"] == "TEST-WPS-001"
        assert status["sensor_type"] == "water_pressure"
        assert status["threshold"] == 30.0
        assert status["simulation_mode"] is True


class TestGasLeakSensor:
    """Tests for GasLeakSensor."""

    @pytest.fixture
    def sensor(self):
        """Create a gas sensor in simulation mode."""
        return GasLeakSensor(
            sensor_id="TEST-GLD-001",
            gas_type=GasType.NATURAL_GAS,
            threshold_ppm=50.0,
            simulation_mode=True,
        )

    def test_initialization(self, sensor):
        """Test sensor initializes correctly."""
        assert sensor.sensor_id == "TEST-GLD-001"
        assert sensor.gas_type == GasType.NATURAL_GAS
        assert sensor.threshold == 50.0
        assert sensor.unit == "PPM"

    def test_check_threshold_normal(self, sensor):
        """Test threshold check with normal levels."""
        severity = sensor.check_threshold(30.0)
        assert severity is None

    def test_check_threshold_warning(self, sensor):
        """Test threshold check with elevated levels."""
        severity = sensor.check_threshold(60.0)
        assert severity == AlertSeverity.WARNING

    def test_check_threshold_danger(self, sensor):
        """Test threshold check with dangerous levels."""
        severity = sensor.check_threshold(120.0)
        assert severity == AlertSeverity.DANGER

    def test_check_threshold_critical(self, sensor):
        """Test threshold check with critical levels."""
        severity = sensor.check_threshold(600.0)
        assert severity == AlertSeverity.CRITICAL

    def test_get_alert_message_warning(self, sensor):
        """Test warning message generation."""
        message = sensor.get_alert_message(60.0, AlertSeverity.WARNING)
        assert "60.0 PPM" in message
        assert "natural gas" in message.lower() or "methane" in message.lower()

    def test_get_alert_message_critical(self, sensor):
        """Test critical message includes evacuation warning."""
        message = sensor.get_alert_message(600.0, AlertSeverity.CRITICAL)
        assert "EVACUATE" in message


class TestSmokeSensor:
    """Tests for SmokeSensor."""

    @pytest.fixture
    def sensor(self):
        """Create a smoke sensor in simulation mode."""
        return SmokeSensor(
            sensor_id="TEST-SMK-001",
            threshold_ppm=10.0,
            location="Kitchen",
            simulation_mode=True,
        )

    def test_initialization(self, sensor):
        """Test sensor initializes correctly."""
        assert sensor.sensor_id == "TEST-SMK-001"
        assert sensor.sensor_type == SensorType.SMOKE
        assert sensor.location == "Kitchen"

    def test_check_threshold(self, sensor):
        """Test smoke threshold detection."""
        assert sensor.check_threshold(5.0) is None
        assert sensor.check_threshold(15.0) == AlertSeverity.WARNING
        assert sensor.check_threshold(25.0) == AlertSeverity.DANGER
        assert sensor.check_threshold(60.0) == AlertSeverity.CRITICAL

    def test_alert_message_includes_location(self, sensor):
        """Test alert message includes location."""
        message = sensor.get_alert_message(15.0, AlertSeverity.WARNING)
        assert "Kitchen" in message


class TestTemperatureSensor:
    """Tests for TemperatureSensor."""

    @pytest.fixture
    def sensor(self):
        """Create a temperature sensor in simulation mode."""
        return TemperatureSensor(
            sensor_id="TEST-TMP-001",
            freeze_threshold_f=35.0,
            high_threshold_f=95.0,
            location="Basement",
            simulation_mode=True,
        )

    def test_initialization(self, sensor):
        """Test sensor initializes correctly."""
        assert sensor.sensor_id == "TEST-TMP-001"
        assert sensor.freeze_threshold == 35.0
        assert sensor.high_threshold == 95.0
        assert sensor.unit == "°F"

    def test_check_threshold_normal(self, sensor):
        """Test normal temperature range."""
        assert sensor.check_threshold(70.0) is None

    def test_check_threshold_freeze_warning(self, sensor):
        """Test freeze warning detection."""
        severity = sensor.check_threshold(38.0)
        assert severity == AlertSeverity.WARNING

    def test_check_threshold_freeze_danger(self, sensor):
        """Test freeze danger detection."""
        severity = sensor.check_threshold(33.0)
        assert severity == AlertSeverity.DANGER

    def test_check_threshold_freeze_critical(self, sensor):
        """Test freeze critical detection."""
        severity = sensor.check_threshold(30.0)
        assert severity == AlertSeverity.CRITICAL

    def test_check_threshold_high_temp(self, sensor):
        """Test high temperature detection."""
        assert sensor.check_threshold(96.0) == AlertSeverity.WARNING
        assert sensor.check_threshold(110.0) == AlertSeverity.DANGER
        assert sensor.check_threshold(125.0) == AlertSeverity.CRITICAL


class TestSensorStatistics:
    """Tests for sensor statistics methods."""

    @pytest.fixture
    def sensor_with_readings(self):
        """Create a sensor with some readings."""
        from src.sensors.base import Reading
        
        sensor = WaterPressureSensor(
            sensor_id="TEST-STATS",
            threshold_psi=30.0,
            simulation_mode=True,
        )
        
        # Add some readings
        for value in [40, 42, 38, 45, 43, 41, 44, 39, 42, 40]:
            sensor.readings.append(Reading(
                sensor_id=sensor.sensor_id,
                sensor_type=sensor.sensor_type,
                value=float(value),
                unit="PSI",
            ))
        
        return sensor

    def test_get_average(self, sensor_with_readings):
        """Test average calculation."""
        avg = sensor_with_readings.get_average(10)
        assert 40 < avg < 43

    def test_get_min(self, sensor_with_readings):
        """Test minimum calculation."""
        min_val = sensor_with_readings.get_min(10)
        assert min_val == 38

    def test_get_max(self, sensor_with_readings):
        """Test maximum calculation."""
        max_val = sensor_with_readings.get_max(10)
        assert max_val == 45

    def test_get_trend_stable(self, sensor_with_readings):
        """Test trend detection with stable readings."""
        trend = sensor_with_readings.get_trend(10)
        assert trend == "stable"
