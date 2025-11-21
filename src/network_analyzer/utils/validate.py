import re
from functools import wraps
from ipaddress import (
    AddressValueError,
    IPv4Address,
    IPv4Network,
    IPv6Address,
    IPv6Network,
    NetmaskValueError,
)
from types import FunctionType

from network_analyzer.utils.scan_models import Targets


class AttemptsError(Exception):
    """Raise when max attempts reached."""


def validate_attempts(max_attempts: int = 5):
    def execute_attempts(func: FunctionType):
        @wraps(func)
        def wrap_attempts(*args, **kwargs):
            for _ in range(max_attempts):
                try:
                    r = func(*args, **kwargs)
                except AttemptsError:
                    pass
                else:
                    return r
            msg = f"Max attempts {max_attempts} to execute {func.__name__}"
            raise TimeoutError(msg)

        return wrap_attempts

    return execute_attempts


@validate_attempts()
def validate_targets(msg: str) -> Targets:
    parsers = (IPv4Address, IPv4Network, IPv6Address, IPv6Network)
    targets_str = input(msg)
    for parser in parsers:
        try:
            return parser(targets_str)
        except (AddressValueError, NetmaskValueError):
            pass
    print("Target no es una IP ni una red válida, intente de nuevo")
    raise AttemptsError


@validate_attempts()
def validate_selections(msg: str) -> str:
    # matches numbers separated by whitespace
    pattern = re.compile(r"^\d+(?:\s+\d+)*$")
    s = input(msg).strip()
    if pattern.match(s):
        return s

    print("Invalid input. Expected format like: 1 2 5")
    raise AttemptsError


@validate_attempts()
def validate_hosts_num(msg: str) -> int:
    val_str = input(msg).strip()

    if val_str.isdigit() and int(val_str) > 0:
        return int(val_str)

    print("No es un número de hosts válido.")
    raise AttemptsError


@validate_attempts()
def validate_state_name(msg: str) -> str:
    name = input(msg)
    if name:
        return name
    print("Nombre de estado esperado inválido.")
    raise AttemptsError
