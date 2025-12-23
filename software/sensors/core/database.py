"""
LUXX HAUS Database Module
SQLAlchemy models and database management.
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import AsyncGenerator, List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
    event,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

from .config import AlertSeverity, GasType, SensorType, get_config


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


# =============================================================================
# DATABASE MODELS
# =============================================================================


class SensorReading(Base):
    """Stores all sensor readings."""

    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    sensor_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    is_alert: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    severity: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    def __repr__(self) -> str:
        return f"<SensorReading {self.sensor_id}: {self.value} {self.unit}>"


class Alert(Base):
    """Stores triggered alerts."""

    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    sensor_type: Mapped[str] = mapped_column(String(30), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    threshold: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Text, nullable=True)
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    acknowledged_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    def __repr__(self) -> str:
        return f"<Alert {self.id}: {self.severity} - {self.sensor_id}>"


class ValveAction(Base):
    """Stores valve open/close actions."""

    __tablename__ = "valve_actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    valve_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    valve_type: Mapped[str] = mapped_column(String(30), nullable=False)
    action: Mapped[str] = mapped_column(String(20), nullable=False)  # open, close
    triggered_by: Mapped[str] = mapped_column(String(100), nullable=False)  # sensor_id or manual
    success: Mapped[bool] = mapped_column(Boolean, default=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    def __repr__(self) -> str:
        return f"<ValveAction {self.valve_id}: {self.action}>"


class SystemEvent(Base):
    """Stores system events and logs."""

    __tablename__ = "system_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    def __repr__(self) -> str:
        return f"<SystemEvent {self.event_type}: {self.message[:50]}>"


class Property(Base):
    """Stores monitored properties (for multi-property support)."""

    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), default="America/Chicago")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Property {self.name}>"


class Sensor(Base):
    """Stores registered sensors."""

    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    sensor_type: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    property_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("properties.id"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    threshold: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    last_reading: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    last_reading_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Sensor {self.sensor_id}: {self.sensor_type}>"


class Valve(Base):
    """Stores registered valves."""

    __tablename__ = "valves"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    valve_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    valve_type: Mapped[str] = mapped_column(String(30), nullable=False)  # water, gas
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    property_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("properties.id"), nullable=True
    )
    is_open: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    gpio_pin: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    last_action: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    last_action_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Valve {self.valve_id}: {'OPEN' if self.is_open else 'CLOSED'}>"


# =============================================================================
# DATABASE MANAGER
# =============================================================================


class DatabaseManager:
    """Manages database connections and operations."""

    def __init__(self, db_url: Optional[str] = None):
        config = get_config()
        self.db_url = db_url or config.database.url

        # Convert sqlite:// to sqlite+aiosqlite:// for async support
        if self.db_url.startswith("sqlite://"):
            self.async_db_url = self.db_url.replace("sqlite://", "sqlite+aiosqlite://")
        else:
            self.async_db_url = self.db_url

        # Sync engine (for migrations and simple operations)
        self.engine = create_engine(self.db_url, echo=config.database.echo)
        self.SessionLocal = sessionmaker(bind=self.engine)

        # Async engine
        self.async_engine = create_async_engine(self.async_db_url, echo=config.database.echo)
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.async_engine, class_=AsyncSession, expire_on_commit=False
        )

    def create_tables(self) -> None:
        """Create all database tables."""
        Base.metadata.create_all(self.engine)

    async def async_create_tables(self) -> None:
        """Create all database tables asynchronously."""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    def drop_tables(self) -> None:
        """Drop all database tables."""
        Base.metadata.drop_all(self.engine)

    def get_session(self):
        """Get a synchronous database session."""
        return self.SessionLocal()

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get an asynchronous database session."""
        async with self.AsyncSessionLocal() as session:
            yield session

    # =========================================================================
    # SENSOR READING OPERATIONS
    # =========================================================================

    async def log_reading(
        self,
        sensor_id: str,
        sensor_type: SensorType,
        value: float,
        unit: str,
        is_alert: bool = False,
        severity: Optional[AlertSeverity] = None,
    ) -> SensorReading:
        """Log a sensor reading."""
        async with self.AsyncSessionLocal() as session:
            reading = SensorReading(
                sensor_id=sensor_id,
                sensor_type=sensor_type.value,
                value=value,
                unit=unit,
                is_alert=is_alert,
                severity=severity.value if severity else None,
            )
            session.add(reading)
            await session.commit()
            await session.refresh(reading)
            return reading

    async def get_recent_readings(
        self,
        sensor_id: str,
        limit: int = 100,
    ) -> List[SensorReading]:
        """Get recent readings for a sensor."""
        async with self.AsyncSessionLocal() as session:
            from sqlalchemy import select

            result = await session.execute(
                select(SensorReading)
                .where(SensorReading.sensor_id == sensor_id)
                .order_by(SensorReading.timestamp.desc())
                .limit(limit)
            )
            return list(result.scalars().all())

    # =========================================================================
    # ALERT OPERATIONS
    # =========================================================================

    async def log_alert(
        self,
        sensor_id: str,
        sensor_type: SensorType,
        value: float,
        threshold: float,
        severity: AlertSeverity,
        message: str,
    ) -> Alert:
        """Log an alert."""
        async with self.AsyncSessionLocal() as session:
            alert = Alert(
                sensor_id=sensor_id,
                sensor_type=sensor_type.value,
                value=value,
                threshold=threshold,
                severity=severity.value,
                message=message,
            )
            session.add(alert)
            await session.commit()
            await session.refresh(alert)
            return alert

    async def get_unacknowledged_alerts(self) -> List[Alert]:
        """Get all unacknowledged alerts."""
        async with self.AsyncSessionLocal() as session:
            from sqlalchemy import select

            result = await session.execute(
                select(Alert)
                .where(Alert.acknowledged == False)
                .order_by(Alert.timestamp.desc())
            )
            return list(result.scalars().all())

    async def acknowledge_alert(
        self,
        alert_id: int,
        acknowledged_by: str = "system",
    ) -> Optional[Alert]:
        """Acknowledge an alert."""
        async with self.AsyncSessionLocal() as session:
            from sqlalchemy import select

            result = await session.execute(select(Alert).where(Alert.id == alert_id))
            alert = result.scalar_one_or_none()

            if alert:
                alert.acknowledged = True
                alert.acknowledged_by = acknowledged_by
                alert.acknowledged_at = datetime.utcnow()
                await session.commit()
                await session.refresh(alert)

            return alert

    # =========================================================================
    # VALVE ACTION OPERATIONS
    # =========================================================================

    async def log_valve_action(
        self,
        valve_id: str,
        valve_type: str,
        action: str,
        triggered_by: str,
        success: bool = True,
        error_message: Optional[str] = None,
    ) -> ValveAction:
        """Log a valve action."""
        async with self.AsyncSessionLocal() as session:
            valve_action = ValveAction(
                valve_id=valve_id,
                valve_type=valve_type,
                action=action,
                triggered_by=triggered_by,
                success=success,
                error_message=error_message,
            )
            session.add(valve_action)
            await session.commit()
            await session.refresh(valve_action)
            return valve_action

    # =========================================================================
    # SYSTEM EVENT OPERATIONS
    # =========================================================================

    async def log_event(
        self,
        event_type: str,
        source: str,
        message: str,
        details: Optional[str] = None,
    ) -> SystemEvent:
        """Log a system event."""
        async with self.AsyncSessionLocal() as session:
            event = SystemEvent(
                event_type=event_type,
                source=source,
                message=message,
                details=details,
            )
            session.add(event)
            await session.commit()
            await session.refresh(event)
            return event


# Singleton database manager
_db_manager: Optional[DatabaseManager] = None


def get_db() -> DatabaseManager:
    """Get the database manager instance."""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


def init_db() -> DatabaseManager:
    """Initialize the database and create tables."""
    db = get_db()
    db.create_tables()
    return db
