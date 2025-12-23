"""
LUXX HAUS Utilities Module
Helper functions and utilities.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from typing import Any, Callable, TypeVar

from loguru import logger


T = TypeVar("T")


def retry_async(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
):
    """
    Decorator for retrying async functions.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries (seconds)
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry
    """
    def decorator(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed: {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
            
            raise last_exception
        
        return wrapper
    return decorator


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9


def psi_to_kpa(psi: float) -> float:
    """Convert PSI to kPa."""
    return psi * 6.89476


def kpa_to_psi(kpa: float) -> float:
    """Convert kPa to PSI."""
    return kpa / 6.89476


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f}h"
    else:
        days = seconds / 86400
        return f"{days:.1f}d"


def format_timestamp(dt: datetime) -> str:
    """Format datetime for display."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def time_ago(dt: datetime) -> str:
    """Get human-readable time ago string."""
    now = datetime.utcnow()
    diff = now - dt
    
    if diff < timedelta(minutes=1):
        return "just now"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() / 60)
        return f"{minutes}m ago"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f"{hours}h ago"
    else:
        days = diff.days
        return f"{days}d ago"


class RateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, max_calls: int, period: float):
        """
        Args:
            max_calls: Maximum calls allowed in period
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls: list[datetime] = []
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> bool:
        """
        Acquire a slot. Returns True if allowed, False if rate limited.
        """
        async with self._lock:
            now = datetime.utcnow()
            cutoff = now - timedelta(seconds=self.period)
            
            # Remove old calls
            self.calls = [t for t in self.calls if t > cutoff]
            
            if len(self.calls) >= self.max_calls:
                return False
            
            self.calls.append(now)
            return True
    
    async def wait(self) -> None:
        """Wait until a slot is available."""
        while not await self.acquire():
            await asyncio.sleep(0.1)


class MovingAverage:
    """Calculate moving average of values."""
    
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.values: list[float] = []
    
    def add(self, value: float) -> float:
        """Add a value and return current average."""
        self.values.append(value)
        if len(self.values) > self.window_size:
            self.values = self.values[-self.window_size:]
        return self.average
    
    @property
    def average(self) -> float:
        """Get current average."""
        if not self.values:
            return 0.0
        return sum(self.values) / len(self.values)
    
    @property
    def min(self) -> float:
        """Get minimum value in window."""
        return min(self.values) if self.values else 0.0
    
    @property
    def max(self) -> float:
        """Get maximum value in window."""
        return max(self.values) if self.values else 0.0
