import subprocess
import logging

logger = logging.getLogger(__name__)

def response(port: int, action: str):
    """Dispatch port action to system-specific function."""
    if not is_valid_port(port):
        logger.error(f"Valor inválido de puerto: {port}")
        return f"Puerto inválido: {port}"

    if action == "cerrar":
        return close_port_linux(port)

    elif action == "abrir":
        return open_port_linux(port)

    else:
        logger.warning(f"Acción desconocida para el puerto {port}: {action}")
        return f"Acción no soportada: {action}"


## Linux-specific implementations

def close_port_linux(port: int):
    """Close a TCP port using nftables by adding a drop rule."""
    cmd = [
        "sudo", "nft", "add", "rule",
        "inet", "filter", "input",
        "tcp", "dport", str(port),
        "drop"
    ]
    output = run(cmd)
    logger.info(f"Closed port {port} via nft. Output: {output}")
    return output

def open_port_linux(port: int):
    """Open a TCP port using nftables by deleting the drop rule for that port."""
    list_cmd = ["sudo", "nft", "list", "chain", "inet", "filter", "input"]
    rules_output = run(list_cmd)

    handle = None
    for line in rules_output.split("\n"):
        if f"tcp dport {port}" in line and "drop" in line:
            parts = line.split()
            if "handle" in parts:
                handle = parts[parts.index("handle") + 1]
                break

    if not handle:
        logger.warning(f"No drop rule found for port {port}. Nothing to open.")
        return f"No rule found for port {port}"

    del_cmd = [
        "sudo", "nft", "delete", "rule",
        "inet", "filter", "input",
        "handle", handle
    ]
    output = run(del_cmd)
    
    logger.info(f"Opened port {port} by removing rule handle {handle}. Output: {output}")
    return output

def is_valid_port(port: int) -> bool:
    return isinstance(port, int) and 1 <= port <= 65535

def run(cmd):
    try:
        p = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )

        if p.returncode != 0:
            logger.error(f"Command failed ({p.returncode}): {p.stderr}")

        return p.stdout.strip() or p.stderr.strip()

    except Exception as e:
        logger.exception(f"Exception while executing command {cmd}: {e}")
        return str(e)
