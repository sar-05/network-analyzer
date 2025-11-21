"""Functions to display menu to create expected Scan Results."""

from pathlib import Path

from network_analyzer.utils.messages import MessagesConfig
from network_analyzer.utils.scan_models import NetworkState, ScanResults
from network_analyzer.utils.validate import (
    validate_hosts_num,
    validate_selections,
    validate_targets,
)


def _print_status(msg: str, p: int | set[str] | None) -> None:
    messages = MessagesConfig.get()
    if p:
        print(f"{msg} {messages.configured}")
    else:
        print(f"{msg}")


def _print_options(msg: str, options: list):
    for i, opt in enumerate(options):
        print(f"{i + 1}) {opt}")
    selections = validate_selections(msg=msg)
    if selections:
        result = []
        for token in selections.split():
            if token.isdigit():
                i = int(token) - 1  # convert to 0-based index
                if 0 <= i < len(options):
                    result.append(options[i])
        return result
    return None


def _print_submenu(
    selection,
    os_list,
    services_list,
    ports_list,
    template: NetworkState,
):
    messages = MessagesConfig.get()
    match selection:
        case "1":
            try:
                template.targets = validate_targets(messages.network_ip)
            except ValueError:
                print(messages.max_attempts)
                raise
        case "2":
            choice = _print_options(messages.select_os, os_list)
            if choice:
                template.host_families = set(choice)
        case "3":
            choice = _print_options(messages.select_services, services_list)
            if choice:
                template.services = set(choice)
        case "4":
            choice = _print_options(messages.select_ports, ports_list)
            if choice:
                template.ports = set(choice)
        case "5":
            choice = validate_hosts_num(messages.expected_devices)
            if choice:
                template.hosts_num = choice
        case _:
            choice = None


def _print_main_menu(
    targets=None,
    os_fams=None,
    services=None,
    ports=None,
    hosts_num=None,
):
    messages = MessagesConfig.get()
    if not targets:
        msg_targets = messages.network_ip_required
        break_msg = messages.break_option_cancel
    else:
        msg_targets = messages.network_ip_configured
        break_msg = messages.break_option_scan.format(targets=targets)

    print(msg_targets)
    _print_status(messages.os_families, os_fams)
    _print_status(messages.services, services)
    _print_status(messages.ports, ports)
    _print_status(messages.devices_num, hosts_num)
    print(break_msg)

    return input(messages.selection_prompt)


def _state_by_menu() -> NetworkState:
    """Display cli menu to create a NetworkState."""
    messages = MessagesConfig.get()
    template = NetworkState()
    print(messages.menu_title)
    os_list = ["Linux", "Windows", "MacOS", "Android", "IOS", "Todos"]
    services_list = ["SSH", "Apache HTTP server", "FTP", "SMTP", "HTTPS"]
    ports_list = [20, 21, 22, 80, 443, 0]
    messages = MessagesConfig.get()
    while True:
        if not template.targets:
            msg_targets = messages.network_ip_required
            break_msg = messages.break_option_cancel
        else:
            msg_targets = messages.network_ip_configured
            break_msg = messages.break_option_scan.format(targets=template.targets)

        print(msg_targets)
        _print_status(messages.os_families, template.host_families)
        _print_status(messages.services, template.services)
        _print_status(messages.ports, template.ports)
        _print_status(messages.devices_num, template.hosts_num)
        print(break_msg)

        selection = input(messages.selection_prompt)
        # selection = _print_main_menu(
        #     template.targets,
        #     template.host_families,
        #     template.services,
        #     template.ports,
        #     template.hosts_num,
        # )
        if selection == "6":
            break
        _print_submenu(
            selection=selection,
            os_list=os_list,
            services_list=services_list,
            ports_list=ports_list,
            template=template,
        )
    return template


def _create_state(state_path):
    """Triggers creation of network state and saves it as JSON."""
    state = _state_by_menu()
    if state.targets:
        with state_path.open("w") as f:
            f.write(state.model_dump_json())
        return state
    msg = "Empty target in template not allowed."
    raise ValueError(msg)


def get_state(states_dir: Path, state_name: str = "default"):
    """Return NetworkState file by name."""
    if not states_dir.exists():
        states_dir.mkdir()
    template_path = states_dir / state_name
    try:
        state_str = template_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return _create_state(template_path)
    else:
        return ScanResults.model_validate_json(state_str)
