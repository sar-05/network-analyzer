from network_analyzer.utils.dispatch_reply import response
import logging

logger = logging.getLogger(__name__)

def execute_reply_actions(data: dict):
    """Process a reply action based on input data."""
    
    results = {}

    for port, action in data.items():
        result = response(int(port), action)
        results[port] = result
        logger.info(f"Procesado puerto {port}: {action} -> {result}")

    print(f"Se han procesado las acciones para {len(data)} puertos.")
    return results

## TESTING PURPOSES
def main():
    sample_data = {
        "8080": "cerrar",
        "9090": "abrir",
        "7070": "cerrar"
    }
    results = execute_reply_actions(sample_data)
    print("Resultados de las acciones:", results)

if __name__ == "__main__":
    main()