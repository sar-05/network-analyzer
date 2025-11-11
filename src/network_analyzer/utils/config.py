import logging
from pathlib import Path

import yaml
from pythonjsonlogger.json import JsonFormatter
from datetime import datetime, UTC

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def _expand_vars(config: dict) -> dict:
    for k, v in config["paths"].items():
        config["paths"][k] = PROJECT_ROOT / v
    return config


def _setup_logging(log_dir):
    log_name = (
        f"network-analyzer-{datetime.now(tz=UTC).strftime('%Y-%m-%dT%H%M%S')}.jsonl"
    )
    log_file = log_dir / log_name
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    formatter = JsonFormatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)

    # Avoid duplicate handlers if setup_logging() is called twice
    if not logger.handlers:
        logger.addHandler(handler)


def load_config(config_file: Path | None = None):
    """Load configuration for network analyzer."""
    if config_file is None:
        config_file = PROJECT_ROOT / "config" / "config.yaml"

    with config_file.open("r") as f:
        config = yaml.safe_load(f)

    config = _expand_vars(config=config)

    log_path = config["paths"]["log_path"]

    if not log_path:
        msg = f"Empty or incomplete paths in config file at {config_file}"
        raise ValueError(msg)

    _setup_logging(log_dir=log_path)

    return config
