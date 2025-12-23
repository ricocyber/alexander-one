"""
LUXX HAUS / ALEXANDER one.1 Sensors Module
All sensor implementations for the smart home protection system.
"""

from .base import BaseSensor, Reading
from .gas_leak import (
    CarbonMonoxideSensor,
    GasLeakSensor,
    MethaneGasSensor,
    PropaneGasSensor,
)
from .motion import KitchenMotionSensor, MotionSensor
from .smoke import PhotoelectricSmokeSensor, SmokeSensor
from .stove_heat import StoveHeatSensor
from .temperature import HumiditySensor, TemperatureSensor
from .water_pressure import HoneywellPX2Sensor, WaterPressureSensor

__all__ = [
    # Base
    "BaseSensor",
    "Reading",
    # Water
    "WaterPressureSensor",
    "HoneywellPX2Sensor",
    # Gas
    "GasLeakSensor",
    "MethaneGasSensor",
    "PropaneGasSensor",
    "CarbonMonoxideSensor",
    # Smoke
    "SmokeSensor",
    "PhotoelectricSmokeSensor",
    # Temperature
    "TemperatureSensor",
    "HumiditySensor",
    # Motion
    "MotionSensor",
    "KitchenMotionSensor",
    # Stove Safety
    "StoveHeatSensor",
]
