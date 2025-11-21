"""Model with functions to setup loging."""

import logging
from datetime import UTC, datetime
from pathlib import Path

from pythonjsonlogger.json import JsonFormatter


def setup_logging(log_path: Path) -> None:
    """Set logging for the project as JSONL."""
    log_name = (
        f"network-analyzer-{datetime.now(tz=UTC).strftime('%Y-%m-%dT%H%M%S')}.jsonl"
    )
    log_file = log_path / log_name
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    formatter = JsonFormatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)

    # Avoid duplicate handlers if setup_logging() is called twice
    if not logger.handlers:
        logger.addHandler(handler)
