"""
LUXX HAUS Configuration Management
Handles loading and validation of system configuration.
"""

from __future__ import annotations

import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings


class GasType(str, Enum):
    NATURAL_GAS = "natural_gas"
    PROPANE = "propane"
    CARBON_MONOXIDE = "carbon_monoxide"
    HYDROGEN_SULFIDE = "hydrogen_sulfide"


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"
    CRITICAL = "critical"


class SensorType(str, Enum):
    WATER_PRESSURE = "water_pressure"
    GAS_LEAK = "gas_leak"
    SMOKE = "smoke"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    ELECTRICAL = "electrical"
    MOTION = "motion"
    STOVE_HEAT = "stove_heat"


# =============================================================================
# SENSOR CONFIGURATIONS
# =============================================================================


class WaterPressureSensorConfig(BaseModel):
    """Configuration for water pressure sensors."""

    enabled: bool = True
    threshold_psi: float = Field(default=30.0, ge=0, le=150)
    critical_threshold_psi: float = Field(default=15.0, ge=0, le=150)
    sample_interval_seconds: float = Field(default=2.0, ge=0.1, le=60)
    auto_shutoff: bool = True
    gpio_pin: Optional[int] = None
    adc_channel: int = 0


class GasLeakSensorConfig(BaseModel):
    """Configuration for gas leak sensors."""

    enabled: bool = True
    gas_type: GasType = GasType.NATURAL_GAS
    threshold_ppm: float = Field(default=50.0, ge=0, le=10000)
    danger_threshold_ppm: float = Field(default=100.0, ge=0, le=10000)
    critical_threshold_ppm: float = Field(default=500.0, ge=0, le=10000)
    sample_interval_seconds: float = Field(default=1.0, ge=0.1, le=60)
    auto_shutoff: bool = True
    gpio_pin: Optional[int] = None
    adc_channel: int = 1


class SmokeSensorConfig(BaseModel):
    """Configuration for smoke sensors."""

    enabled: bool = True
    threshold_ppm: float = Field(default=10.0, ge=0, le=1000)
    sample_interval_seconds: float = Field(default=1.0, ge=0.1, le=60)
    gpio_pin: Optional[int] = None
    adc_channel: int = 2


class TemperatureSensorConfig(BaseModel):
    """Configuration for temperature sensors."""

    enabled: bool = True
    freeze_threshold_f: float = Field(default=35.0, ge=-40, le=150)
    high_threshold_f: float = Field(default=95.0, ge=0, le=200)
    sample_interval_seconds: float = Field(default=10.0, ge=1, le=300)
    gpio_pin: int = 4


class StoveSafetyConfig(BaseModel):
    """Configuration for stove safety system."""

    enabled: bool = True
    heat_threshold_f: float = Field(default=150.0, ge=100, le=500)
    danger_threshold_f: float = Field(default=300.0, ge=100, le=600)
    unattended_timeout_seconds: float = Field(default=300.0, ge=60, le=1800)
    warning_timeout_seconds: float = Field(default=180.0, ge=30, le=900)
    sample_interval_seconds: float = Field(default=2.0, ge=0.5, le=30)
    auto_shutoff: bool = True
    heat_sensor_gpio_pin: int = 24
    motion_sensor_gpio_pin: int = 23
    gas_valve_gpio_pin: int = 27


class SensorsConfig(BaseModel):
    """Combined sensor configuration."""

    water_pressure: WaterPressureSensorConfig = WaterPressureSensorConfig()
    gas_leak: GasLeakSensorConfig = GasLeakSensorConfig()
    smoke: SmokeSensorConfig = SmokeSensorConfig()
    temperature: TemperatureSensorConfig = TemperatureSensorConfig()
    stove_safety: StoveSafetyConfig = StoveSafetyConfig()


# =============================================================================
# VALVE CONFIGURATIONS
# =============================================================================


class WaterValveConfig(BaseModel):
    """Configuration for water main valve."""

    enabled: bool = True
    gpio_pin: int = 17
    normally_open: bool = True
    activation_delay_seconds: float = 0.5


class GasValveConfig(BaseModel):
    """Configuration for gas valve."""

    enabled: bool = True
    gpio_pin: int = 27
    normally_open: bool = False
    activation_delay_seconds: float = 0.5


class ValvesConfig(BaseModel):
    """Combined valve configuration."""

    water: WaterValveConfig = WaterValveConfig()
    gas: GasValveConfig = GasValveConfig()


# =============================================================================
# NOTIFICATION CONFIGURATIONS
# =============================================================================


class PushNotificationConfig(BaseModel):
    """Firebase push notification configuration."""

    enabled: bool = False
    firebase_credentials_path: Optional[str] = None
    default_topic: str = "luxx_haus_alerts"


class SMSNotificationConfig(BaseModel):
    """Twilio SMS notification configuration."""

    enabled: bool = False
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    from_number: Optional[str] = None


class EmailNotificationConfig(BaseModel):
    """Email notification configuration."""

    enabled: bool = False
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    from_address: Optional[str] = None


class NotificationsConfig(BaseModel):
    """Combined notification configuration."""

    push: PushNotificationConfig = PushNotificationConfig()
    sms: SMSNotificationConfig = SMSNotificationConfig()
    email: EmailNotificationConfig = EmailNotificationConfig()
    
    # Alert escalation settings
    warning_channels: List[str] = ["push"]
    danger_channels: List[str] = ["push", "sms"]
    critical_channels: List[str] = ["push", "sms", "email"]


# =============================================================================
# CONTACT CONFIGURATION
# =============================================================================


class EmergencyContact(BaseModel):
    """Emergency contact information."""

    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    notify_on: List[AlertSeverity] = [AlertSeverity.DANGER, AlertSeverity.CRITICAL]


# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================


class DatabaseConfig(BaseModel):
    """Database configuration."""

    url: str = "sqlite:///luxx_haus.db"
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10


# =============================================================================
# API CONFIGURATION
# =============================================================================


class APIConfig(BaseModel):
    """API server configuration."""

    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    cors_origins: List[str] = ["*"]
    api_key: Optional[str] = None


# =============================================================================
# SYSTEM CONFIGURATION
# =============================================================================


class SystemConfig(BaseModel):
    """System-level configuration."""

    name: str = "LUXX HAUS"
    location: str = "Home"
    timezone: str = "America/Chicago"
    log_level: str = "INFO"
    simulation_mode: bool = False  # Set to True for testing without hardware


# =============================================================================
# MAIN CONFIGURATION
# =============================================================================


class LuxxHausConfig(BaseModel):
    """Main LUXX HAUS configuration."""

    system: SystemConfig = SystemConfig()
    sensors: SensorsConfig = SensorsConfig()
    valves: ValvesConfig = ValvesConfig()
    notifications: NotificationsConfig = NotificationsConfig()
    emergency_contacts: List[EmergencyContact] = []
    database: DatabaseConfig = DatabaseConfig()
    api: APIConfig = APIConfig()

    @classmethod
    def from_yaml(cls, path: str | Path) -> "LuxxHausConfig":
        """Load configuration from YAML file."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        with open(path, "r") as f:
            data = yaml.safe_load(f)

        return cls.model_validate(data or {})

    @classmethod
    def from_env(cls) -> "LuxxHausConfig":
        """Load configuration from environment variables."""
        config_path = os.getenv("LUXX_HAUS_CONFIG")
        if config_path:
            return cls.from_yaml(config_path)

        # Build config from individual env vars
        return cls(
            system=SystemConfig(
                name=os.getenv("LUXX_HAUS_NAME", "LUXX HAUS"),
                location=os.getenv("LUXX_HAUS_LOCATION", "Home"),
                timezone=os.getenv("LUXX_HAUS_TIMEZONE", "America/Chicago"),
                simulation_mode=os.getenv("LUXX_HAUS_SIMULATION", "false").lower() == "true",
            ),
            database=DatabaseConfig(
                url=os.getenv("LUXX_HAUS_DB_URL", "sqlite:///luxx_haus.db"),
            ),
            api=APIConfig(
                host=os.getenv("LUXX_HAUS_API_HOST", "0.0.0.0"),
                port=int(os.getenv("LUXX_HAUS_API_PORT", "8000")),
            ),
        )

    def to_yaml(self, path: str | Path) -> None:
        """Save configuration to YAML file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False, sort_keys=False)


# Singleton config instance
_config: Optional[LuxxHausConfig] = None


def get_config() -> LuxxHausConfig:
    """Get the current configuration instance."""
    global _config
    if _config is None:
        _config = LuxxHausConfig.from_env()
    return _config


def set_config(config: LuxxHausConfig) -> None:
    """Set the configuration instance."""
    global _config
    _config = config


def load_config(path: str | Path) -> LuxxHausConfig:
    """Load configuration from file and set as current."""
    config = LuxxHausConfig.from_yaml(path)
    set_config(config)
    return config
