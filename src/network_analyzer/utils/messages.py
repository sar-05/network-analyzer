"""Module to handle menu message parsing and initialization."""

import logging
from pathlib import Path

from pydantic import BaseModel
from yaml import YAMLError, safe_load

logger = logging.getLogger(__name__)


class Messages(BaseModel):
    """Model to validate display messages."""

    menu_title: str
    network_ip: str
    select_os: str
    select_services: str
    select_ports: str
    expected_devices: str
    configured: str
    cancel: str
    scan: str
    selection_prompt: str
    max_attempts: str
    max_attempts_exit: str
    network_ip_required: str
    network_ip_configured: str
    os_families: str
    services: str
    ports: str
    devices_num: str
    break_option_cancel: str
    break_option_scan: str
    cancel_operation: str


class MessagesConfig:
    """Singleton to manage menu messages."""

    _instance: Messages | None = None

    @classmethod
    def initialize(cls, config_dir: Path, lang: str):
        """Init Messages instance from YAML file."""
        config_path = config_dir / f"{lang}_messages.yaml"
        try:
            with config_path.open("r", encoding="utf-8") as f:
                config_data = safe_load(f)
        except FileNotFoundError:
            logger.fatal("Menu messages for %s not found.", lang)
            raise
        except YAMLError:
            logger.fatal("Error while parsing %s", config_path)
            raise
        else:
            cls._instance = Messages.model_validate(config_data["messages"])

    @classmethod
    def get(cls) -> Messages:
        """Expose Messages instance."""
        if cls._instance is None:
            msg = "MessagesConfig not initialized."
            raise RuntimeError(msg)
        return cls._instance
