"""Main acces point for network-analyzer."""

import logging
from pathlib import Path

from pyfiglet import figlet_format

from network_analyzer.utils.config import load_config
from network_analyzer.utils.menu import get_state
from network_analyzer.utils.messages import MessagesConfig
from network_analyzer.utils.setup_logging import setup_logging
from network_analyzer.utils.validate import validate_state_name

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main():
    """Orchestrate network-analyzer execution."""
    # Load base and logging configs.
    config = load_config(project_root=PROJECT_ROOT)
    log_path = config.paths.logs
    setup_logging(log_path=log_path)
    logger = logging.getLogger(__name__)
    logger.info("Started network-analyzer.")

    messages = config.paths.messages

    print(figlet_format("network-analyzer"))

    # Initialize menu messages
    MessagesConfig.initialize(messages, "es")

    state_name = validate_state_name("Ingrese el estado a crear o cargar: ")
    states_dir = config.paths.states
    state = get_state(states_dir, state_name)
    print(state.model_dump_json(indent=2))

    # Add environment checks

    # Create template if not available and load it.
    # state_dir =
    # template_dir = config["paths"]["data"] / "templates"
    # try:
    #     template = get_template(template_dir=template_dir)
    #     logger.info("Template found at %s", template_dir)
    # except FileNotFoundError:
    #     logger.info("Creating new template")
    #     print("No se ha encontrado configuración.")
    #     create_template(template_dir=template_dir)
    #     template = get_template(template_dir=template_dir)
    # except ValidationError:
    #     logger.warning("Failed to validate template %s", template_dir)
    #     logger.warning("Attempting to create valid template")
    #     create_template(template_dir=template_dir)

    # Scan the network and acquire the results
    # targets = "192.168.100.0/24"
    # scan = acquire(targets=targets)

    # Analyze the results and identify possible actions
    # actions = analyze(scan, template)

    # Execute containmaint actions
    # contain(actions)


if __name__ == "__main__":
    main()
