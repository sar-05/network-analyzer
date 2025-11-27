"""Main acces point for network-analyzer."""

import logging
from pathlib import Path

from pyfiglet import figlet_format

from network_analyzer.acquisition.acquire import acquire as ac
from network_analyzer.analysis.ai_analyze_report import reporte_analisis_ia
from network_analyzer.utils.config import load_config
from network_analyzer.utils.menu import get_state
from network_analyzer.utils.messages import MessagesConfig
from network_analyzer.utils.scan_models import ToJson
from network_analyzer.utils.setup_logging import setup_logging

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main():
    """Orchestrate network-analyzer execution."""
    # Load base and logging configs.
    config = load_config(project_root=PROJECT_ROOT)
    log_path = config.paths.logs
    setup_logging(log_path=log_path)
    logger = logging.getLogger(__name__)
    logger.info("Started network-analyzer.")

    messages_path = config.paths.messages

    print(figlet_format("network-analyzer", width=200))

    # Initialize menu messages
    MessagesConfig.initialize(messages_path, "es")
    # messages = MessagesConfig.get()

    # Create state and save it to JSON file.
    states_dir = config.paths.data / "states"
    state, state_path = get_state(states_dir=states_dir)
    targets = state.targets

    # Scan the network and acquire the results
    if not targets:
        msg = "Template withouth Target"
        raise ValueError(msg)

    # Use nmap to scan the target.
    scan = ac(targets=targets)

    if not scan:
        print("El escaneo no econtró detalles")
        return

    to_json = ToJson(state=state, scan=scan)

    with state_path.open("w", encoding="UTF-8") as f:
        f.write(to_json.model_dump_json(indent=2))

    ai_result = reporte_analisis_ia(
        archivo_json=state_path,
        archivo_api_key=config.paths.api_key,
        archivo_prompt=config.paths.prompt_ai,
    )

    if not ai_result:
        print("No se ha podido contactar la IA")
        return

    result_md = Path("/home/sar/Repos/network-analyzer/outputs/results.md")
    with result_md.open("w", encoding="UTF-8") as f:
        f.write(ai_result)


if __name__ == "__main__":
    main()
