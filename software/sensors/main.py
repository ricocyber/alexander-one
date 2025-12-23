"""
LUXX HAUS Smart Home Protection System
Main entry point.
"""

from __future__ import annotations

import argparse
import asyncio
import signal
import sys
from pathlib import Path

from loguru import logger

from .core import LuxxHausConfig, get_config, init_db, load_config
from .core.monitor import LuxxHausMonitor, create_default_monitor, run_demo


def setup_logging(level: str = "INFO") -> None:
    """Configure logging."""
    logger.remove()
    logger.add(
        sys.stderr,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        level=level,
    )
    logger.add(
        "logs/luxx_haus_{time}.log",
        rotation="1 day",
        retention="7 days",
        level="DEBUG",
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="LUXX HAUS Smart Home Protection System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main                     # Run with default config
  python -m src.main --config config.yaml
  python -m src.main --simulation        # Run in simulation mode
  python -m src.main --api               # Run with API server
  python -m src.main --demo              # Run quick demo
        """,
    )
    
    parser.add_argument(
        "-c", "--config",
        type=str,
        help="Path to configuration file (YAML)",
    )
    
    parser.add_argument(
        "-s", "--simulation",
        action="store_true",
        help="Run in simulation mode (no hardware)",
    )
    
    parser.add_argument(
        "--api",
        action="store_true",
        help="Start REST API server",
    )
    
    parser.add_argument(
        "--api-host",
        type=str,
        default="0.0.0.0",
        help="API server host (default: 0.0.0.0)",
    )
    
    parser.add_argument(
        "--api-port",
        type=int,
        default=8000,
        help="API server port (default: 8000)",
    )
    
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run a quick demo",
    )
    
    parser.add_argument(
        "--demo-duration",
        type=int,
        default=30,
        help="Demo duration in seconds (default: 30)",
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    
    parser.add_argument(
        "--init-db",
        action="store_true",
        help="Initialize database and exit",
    )
    
    parser.add_argument(
        "--generate-config",
        type=str,
        metavar="PATH",
        help="Generate default config file at PATH and exit",
    )
    
    return parser.parse_args()


async def run_monitor(
    config_path: str | None = None,
    simulation_mode: bool = False,
) -> None:
    """Run the monitoring system."""
    # Load config
    if config_path:
        load_config(config_path)
    
    config = get_config()
    if simulation_mode:
        config.system.simulation_mode = True
    
    # Create and configure monitor
    monitor = create_default_monitor(simulation_mode=config.system.simulation_mode)
    
    # Setup signal handlers
    loop = asyncio.get_running_loop()
    
    async def shutdown():
        logger.info("Received shutdown signal")
        await monitor.stop()
    
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig,
            lambda: asyncio.create_task(shutdown()),
        )
    
    # Run monitor
    try:
        async with monitor:
            await monitor.start()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    finally:
        await monitor.stop()


def run_api_server(host: str, port: int) -> None:
    """Run the API server."""
    from .api import run_server
    run_server(host=host, port=port)


def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(log_level)
    
    logger.info("🏠 LUXX HAUS Smart Home Protection System")
    
    # Generate config and exit
    if args.generate_config:
        config = LuxxHausConfig()
        config.to_yaml(args.generate_config)
        logger.info(f"Generated config at: {args.generate_config}")
        return 0
    
    # Init database and exit
    if args.init_db:
        init_db()
        logger.info("Database initialized")
        return 0
    
    # Load config
    if args.config:
        load_config(args.config)
    
    # Run demo
    if args.demo:
        logger.info(f"Running demo for {args.demo_duration} seconds...")
        asyncio.run(run_demo(args.demo_duration))
        return 0
    
    # Run API server
    if args.api:
        logger.info(f"Starting API server at {args.api_host}:{args.api_port}")
        run_api_server(args.api_host, args.api_port)
        return 0
    
    # Run monitor
    try:
        asyncio.run(run_monitor(
            config_path=args.config,
            simulation_mode=args.simulation,
        ))
    except KeyboardInterrupt:
        pass
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
