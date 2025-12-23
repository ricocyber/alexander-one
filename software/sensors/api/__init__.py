"""
LUXX HAUS API Module
FastAPI REST API for the smart home protection system.
"""

from .app import app, run_server

__all__ = ["app", "run_server"]
