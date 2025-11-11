from network_analyzer.acquisition.acquire import acquire
from network_analyzer.utils.config import load_config
import logging


def main():
    load_config()
    logger = logging.getLogger(__name__)
    logger.info("Test Log")
    targets = "192.168.100.0/24"
    scan = acquire(targets=targets)
    if scan:
        print(scan.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
