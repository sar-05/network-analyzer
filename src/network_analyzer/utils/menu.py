"""Functions to display menu to create expected Scan Results."""

from enum import Enum
import logging
from pathlib import Path
from re import compile as comp
from typing import Any

from pydantic import BaseModel, Field, ValidationError

from network_analyzer.utils.max_attempts import (
    AttemptError,
    max_attempts,
)
from network_analyzer.utils.messages import MessagesConfig
from network_analyzer.utils.scan_models import NetworkState, Targets

logger = logging.getLogger(__name__)


class FieldType(Enum):
    """Enum to track what NetworkState field a menu represents."""

    TARGETS = "targets"
    HOSTS_NUM = "hosts_num"
    HOST_FAMILIES = "host_families"
    PORTS = "ports"
    SERVICES = "services"


class MenuOption(BaseModel):
    """Model for option in a menu."""

    value: str | int | Targets
    field_type: FieldType | None = None
    required: bool = False
    status: bool = False
    custom: bool = False

    def set_status(self):
        value = self.value
        if self.status:
            value = f"{value}, (Configurado)"

    def set_required(self):
        value = self.value
        if self.required:
            value = f"{value}, (Necesario)"

    # @max_attempts()
    def resolve_custom(self):
        if self.status and self.custom:
            user_input = input("Ingrese user input: ")
            try:
                match self.field_type:
                    case (
                        FieldType.HOST_FAMILIES | FieldType.SERVICES | FieldType.TARGETS
                    ):
                        logger.debug("Match con str")
                        self.value = user_input
                    case FieldType.HOSTS_NUM | FieldType.PORTS:
                        logger.debug("Match con int")
                        self.value = int(user_input)
            except (ValidationError, ValueError) as e:
                msg = f"Error while resolving custom value {user_input}"
                raise AttemptError(msg) from e
            else:
                print(self.value)
        else:
            return


class MenuSelection(BaseModel):
    """Model for a valid selection of options."""

    selection_idxs: list[int] = Field(default_factory=list)
    field_type: FieldType | None = None
    selection_options: list[MenuOption] = Field(default_factory=list)

    @max_attempts(input_param="selection_str")
    def get_indices(self, selection_str: str) -> list[int]:
        """Set selection_idxs or raises AttemptError."""
        # pattern = comp(r"^\d+(?:\s+\d+)*$")
        pattern = comp(r"^(?:\d+(?:\s+\d+)*|(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?)$")
        s = selection_str.strip()
        if not pattern.match(s):
            logger.warning(f"Unable to parse {s} as indexes.")
            raise AttemptError
        idxs = [int(i) - 1 for i in s.split()]
        self.selection_idxs = idxs
        return idxs

    def indices_to_options(self, options: list[MenuOption]):
        """Populate instance selection_options with options in selection_idxs."""
        selection_options = self.selection_options
        valid_range = range(len(options))
        for i in self.selection_idxs:
            if i in valid_range:
                option = options[i]
                option.status = True
                option.resolve_custom()
                selection_options.append(option)
            else:
                logger.warning(
                    "Invalid index '%d' discarded for range %s",
                    i,
                    valid_range,
                )
        self.selection_options = selection_options


class MenuClass(BaseModel):
    """Model for a menu to define selections."""

    options: list[MenuOption] = Field(default_factory=list)
    field_type: FieldType | None = None
    selection: list[MenuOption] | None = None
    custom: MenuOption | list[MenuOption] | None = None

    def from_list(self, opts: list[Any], field_type: FieldType | None = None):
        """Create a list of MenuOption items given a list."""
        self.field_type = field_type
        custom = False
        for opt in opts:
            if opt == "CUSTOM" or opt == 1000:
                custom = True
            logger.debug("opt es %s y custom es %s", opt, custom)
            opt_obj = MenuOption(value=opt, custom=custom, field_type=field_type)
            self.options.append(opt_obj)

    def print_options(self):
        """Pretty print options."""
        options = self.options
        for i, opt in enumerate(options):
            print(f"{i + 1}) {opt.value}")

    def get_selection(self) -> list[MenuOption]:
        """Populate menu selection."""
        selection = MenuSelection(field_type=self.field_type)
        selection.get_indices()
        options = self.options
        if not options:
            msg = "Unable to bind empty options to selections."
            logger.exception(msg)
            raise ValueError(msg)
        selection.indices_to_options(self.options)
        self.selection = selection.selection_options
        return self.selection


def parse_menu_selection(
    field_type: FieldType,
    selection: list[MenuOption] | None = None,
) -> Targets | int | set[str] | set[int]:
    """Parse menu selection to appropriate NetworkState type."""

    if not selection:
        raise ValueError("Empty selection")

    match field_type:
        case FieldType.TARGETS:
            # Assuming only one target is selected

            if len(selection) != 1:
                raise ValueError("Expected single target selection")

            value = selection[0].value

            if isinstance(value, Targets):
                return value

            try:
                target = Targets()
                target.from_string(value=value)
            except (ValidationError, ValueError):
                msg = f"Unable to parse {selection[0]} as Targets object"
                raise TypeError(msg)
            else:
                return target

        case FieldType.HOSTS_NUM:
            # Assuming only one number is selected
            if len(selection) != 1:
                raise ValueError("Expected single number selection")
            value = selection[0].value
            if not isinstance(value, int):
                raise TypeError(f"Expected int, got {type(value)}")
            return value

        case FieldType.HOST_FAMILIES | FieldType.SERVICES:
            # Return set of strings
            result = set()
            for opt in selection:
                if not isinstance(opt.value, str):
                    raise TypeError(f"Expected str, got {type(opt.value)}")
                result.add(opt.value)
            return result

        case FieldType.PORTS:
            # Return set of ints
            result = set()
            for opt in selection:
                if not isinstance(opt.value, int):
                    raise TypeError(f"Expected int, got {type(opt.value)}")
                result.add(opt.value)
            return result

        case _:
            raise ValueError(f"Unknown field type: {field_type}")


def sub_menu(
    sub_options: list[Any] | None, field_type: FieldType
) -> Targets | int | set[str] | set[int]:
    sub_menu = MenuClass(field_type=field_type)
    if not sub_options:
        return parse_menu_selection(field_type=field_type)
    sub_menu.from_list(sub_options, field_type)
    sub_menu.print_options()
    selection = sub_menu.get_selection()
    return parse_menu_selection(selection=selection, field_type=field_type)


def main_menu() -> NetworkState:
    messages = MessagesConfig.get()
    state = NetworkState(
        host_families=set(messages.os_opts),
        hosts_num=5,
        ports=set(messages.ports_opts),
        services=set(messages.services_opts),
    )

    main_menu = MenuClass()
    main_menu.from_list(messages.main_menu_opts)

    while True:
        main_menu.print_options()
        selection = main_menu.get_selection()[0].value

        match selection:
            case "Ip de Red":
                result = sub_menu(messages.ip_opts, FieldType.TARGETS)
                state.targets = result
            case "Familia de OS":
                result = sub_menu(messages.os_opts, FieldType.HOST_FAMILIES)
                state.host_families = result
            case "Servicios":
                result = sub_menu(messages.services_opts, FieldType.SERVICES)
                state.services = result
            case "Puertos":
                result = sub_menu(messages.ports_opts, FieldType.PORTS)
                state.ports = result
            case "Número de Dispositivos":
                result = sub_menu(messages.num_dev_opts, FieldType.HOSTS_NUM)
                state.hosts_num = result
            case "Escanear":
                break
            case _:
                logger.error("%s", messages.unknown_menu_opt)
                print(messages.unknown_menu_opt)

    return state


def get_state(states_dir: Path, state_name: str = "default"):
    """Return NetworkState file by name."""
    if not states_dir.exists():
        states_dir.mkdir()
    state_name = state_name + ".json"
    state_path = states_dir / state_name
    state = main_menu()
    if state.targets:
        return state, state_path
    msg = "Empty target in template not allowed."
    raise ValueError(msg)
