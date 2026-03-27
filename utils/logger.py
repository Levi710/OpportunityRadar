"""Loguru setup for structured logging across OpportunityRadar."""

import sys
from pathlib import Path
from loguru import logger


def setup_logger():
    """Configure loguru for console and file logging.

    Removes default handler and adds:
    - Console handler with INFO level and colored output.
    - File handler with DEBUG level, daily rotation, and 7-day retention.
    """
    logger.remove()

    # Console output — INFO and above
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan> | "
               "<level>{message}</level>",
        colorize=True,
    )

    # File output — DEBUG and above, rotated daily
    log_dir = Path(__file__).resolve().parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    logger.add(
        str(log_dir / "opportunityradar_{time:YYYY-MM-DD}.log"),
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} | {message}",
        rotation="1 day",
        retention="7 days",
        encoding="utf-8",
    )

    return logger
