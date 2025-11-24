"""Functions to display menu to create expected Scan Results."""

import logging
from re import compile as comp

from pydantic import BaseModel, Field

from network_analyzer.utils.max_attempts import (
    AttemptError,
    max_attempts,
)

logger = logging.getLogger(__name__)


class MenuOption(BaseModel):
    """Model for option in a menu."""

    value: str | int
    status: bool = False


class MenuSelection(BaseModel):
    """Model for a valid selection of options."""

    selection_idxs: list[int] = Field(default_factory=list)
    selection_options: list[MenuOption] = Field(default_factory=list)

    @max_attempts(input_param="selection_str")
    def get_indices(self, selection_str: str) -> list[int]:
        """Set selection_idxs or raises AttemptError."""
        pattern = comp(r"^\d+(?:\s+\d+)*$")
        s = selection_str.strip()
        if not pattern.match(s):
            print(f"Unable to parse {s} as indexes.")
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
    selection: list[MenuOption] | None = None
    custom: MenuOption | list[MenuOption] | None = None

    def from_list(self, opts: list):
        """Create a list of MenuOption items given a list."""
        for opt in opts:
            opt_obj = MenuOption(value=opt)
            self.options.append(opt_obj)

    def print_options(self):
        """Pretty print options."""
        options = self.options
        for i, opt in enumerate(options):
            print(f"{i + 1}) {opt.value}")

    def get_selection(self):
        """Populate menu selection."""
        selection = MenuSelection()
        selection.get_indices()
        options = self.options
        if not options:
            msg = "Unable to bind empty options to selections."
            logger.exception(msg)
            raise ValueError(msg)
        selection.indices_to_options(self.options)
        self.selection = selection.selection_options


if __name__ == "__main__":
    menu = MenuClass()
    menu.from_list(["Test 1", "Test 2", "Test 3"])
    menu.print_options()
    menu.get_selection()
    print(menu.selection)


# def _print_status(msg: str, p: int | set[str] | set[int] | None) -> None:
#     messages = MessagesConfig.get()
#     if p:
#         print(f"{msg} {messages.configured}")
#     else:
#         print(f"{msg}")
#
#
# def _print_options(msg: str, options: list):
#     for i, opt in enumerate(options):
#         print(f"{i + 1}) {opt}")
#     selections = validate_selections(msg=msg)
#     if selections:
#         result = []
#         for token in selections.split():
#             if token.isdigit():
#                 i = int(token) - 1  # convert to 0-based index
#                 if 0 <= i < len(options):
#                     result.append(options[i])
#         return result
#     return None
#
#
# def _print_submenu(
#     selection,
#     os_list,
#     services_list,
#     ports_list,
#     status: NetworkState,
# ):
#     messages = MessagesConfig.get()
#     match selection:
#         case "1":
#             try:
#                 status.targets = validate_targets(messages.network_ip)
#             except ValueError:
#                 print(messages.max_attempts)
#                 raise
#         case "2":
#             choice = _print_options(messages.select_os, os_list)
#             if choice:
#                 status.host_families = set(choice)
#         case "3":
#             choice = _print_options(messages.select_services, services_list)
#             if choice:
#                 status.services = set(choice)
#         case "4":
#             choice = _print_options(messages.select_ports, ports_list)
#             if choice:
#                 status.ports = set(choice)
#         case "5":
#             choice = validate_hosts_num(messages.expected_devices)
#             if choice:
#                 status.hosts_num = choice
#         case _:
#             choice = None
#
#
# def _state_by_menu() -> NetworkState:
#     """Display cli menu to create a NetworkState."""
#     messages = MessagesConfig.get()
#     state = NetworkState()

#     # TODO: Move opotions lists to messages

#     os_list = ["Linux", "Windows", "MacOS", "Android", "IOS", "Todos"]
#     services_list = ["SSH", "Apache HTTP server", "FTP", "SMTP", "HTTPS"]
#     ports_list = [20, 21, 22, 80, 443, 0]
#     print(messages.menu_title)
#     while True:
#         if not state.targets:
#             msg_targets = messages.network_ip_required
#             break_msg = messages.break_option_cancel
#         else:
#             msg_targets = messages.network_ip_configured
#             break_msg = messages.break_option_scan.format(targets=state.targets)
#
#         print(msg_targets)
#         _print_status(messages.os_families, state.host_families)
#         _print_status(messages.services, state.services)
#         _print_status(messages.ports, state.ports)
#         _print_status(messages.devices_num, state.hosts_num)
#         print(break_msg)
#
#         selection = input(messages.selection_prompt)
#         if selection == "6":
#             print(messages.cancel_operation)
#             break
#         _print_submenu(
#             selection=selection,
#             os_list=os_list,
#             services_list=services_list,
#             ports_list=ports_list,
#             status=state,
#         )
#     return state
#
#
# def _create_state(state_path: Path) -> NetworkState:
#     """Triggers creation of network state and saves it as JSON."""
#     state = _state_by_menu()
#     if state.targets:
#         with state_path.open("w") as f:
#             f.write(state.model_dump_json())
#         return state
#     msg = "Empty target in template not allowed."
#     raise ValueError(msg)
#
#
# def get_state(states_dir: Path, state_name: str = "default"):
#     """Return NetworkState file by name."""
#     if not states_dir.exists():
#         states_dir.mkdir()
#     template_path = states_dir / state_name / ".json"
#     try:
#         state_str = template_path.read_text(encoding="utf-8")
#     except FileNotFoundError:
#         return _create_state(template_path)
#     else:
#         return ScanResults.model_validate_json(state_str)
