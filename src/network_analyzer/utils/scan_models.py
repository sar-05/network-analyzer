"""Pydantic models for use over the project."""

from ipaddress import (
    IPv4Address,
    IPv4Network,
    IPv6Address,
    IPv6Network,
    AddressValueError,
    NetmaskValueError,
)

from pydantic import BaseModel, Field, field_serializer


class Targets(BaseModel):
    value: IPv4Address | IPv6Address | IPv4Network | IPv6Network | None = None

    @property
    def parsed(self) -> IPv4Address | IPv6Address | IPv4Network | IPv6Network | None:
        """Returns the parsed IP object directly"""
        return self.value

    def from_string(
        self, value: str | int
    ) -> IPv4Address | IPv6Address | IPv4Network | IPv6Network:
        """
        Parse and return the IP object directly.
        Returns:
            The parsed IPv4Address, IPv6Address, IPv4Network, or IPv6Network object
        """
        for parser in [IPv4Address, IPv6Address, IPv4Network, IPv6Network]:
            try:
                self.value = parser(value)
                return self.value
            except (AddressValueError, NetmaskValueError, ValueError):
                continue
        raise ValueError(f"'{value}' is not a valid IPv4/IPv6 address or network")


class ServiceInfo(BaseModel):
    """Model for service information."""

    name: str | None = None
    product: str | None = None
    version: str | None = None
    confidence: int | None = None
    extrainfo: str | None = None


class PortInfo(BaseModel):
    """Model for port information."""

    port: int
    protocol: str
    state: str
    reason: str | None = None
    service: ServiceInfo | None = None


class OSMatchInfo(BaseModel):
    """Model for OS match information."""

    type: str | None
    vendor: str | None
    family: str | None


class OSMatch(BaseModel):
    """Model for OS Match properties."""

    name: str | None
    accuracy: int | None
    info: dict[int, OSMatchInfo]


class HostInfo(BaseModel):
    """Model for host information."""

    address: IPv4Address | IPv6Address
    hostname: list[str] | None = None
    state: str
    reason: str | None = None
    scan_time: str | None = None


class JsonHost(BaseModel):
    """Model for host properties."""

    host_info: HostInfo
    best_match: OSMatch | None = None
    ports: dict[int, PortInfo] = Field(default_factory=dict)


class ScanResults(BaseModel):
    """Model for scan results."""

    targets: Targets
    hosts: dict[str, JsonHost] = {}

    def __getitem__(self, key: str) -> JsonHost:
        return self.hosts[key]

    def __setitem__(self, key: str, value: JsonHost) -> None:
        self.hosts[key] = value

    def __delitem__(self, key: str) -> None:
        del self.hosts[key]

    def update(self, other: dict[str, JsonHost]) -> None:
        """Update the hosts dict with another dict of host-objects."""
        for k, v in other.items():
            if not isinstance(v, JsonHost):
                msg = f"Expected JsonHost, got {type(v)} for key {k}"
                raise TypeError(msg)
        self.hosts.update(other)


class NetworkState(BaseModel):
    """Model for the network state, a scan summary.

    It's meant to be use for comparing expected results against actual results.
    """

    targets: Targets | None = None
    hosts_num: int | None = None
    host_families: set[str] | None = None
    ports: set[int] | None = None
    services: set[str] | None = None

    @classmethod
    def from_scan_results(cls, scan_results: ScanResults) -> "NetworkState":
        """Create a summary template from scan results."""
        host_families = set()
        ports = set()
        services = set()

        for host in scan_results.hosts.values():
            if host.best_match and host.best_match.info:
                for os_info in host.best_match.info.values():
                    if os_info.type:
                        host_families.add(os_info.family)

            for port_info in host.ports.values():
                ports.add(port_info.port)
                if port_info.service and port_info.service.name:
                    services.add(port_info.service.name)

        return cls(
            targets=scan_results.targets,
            hosts_num=len(scan_results.hosts),
            host_families=host_families or None,
            ports=ports or None,
            services=services or None,
        )

    @field_serializer("targets")
    def serialize_targets(self, targets: Targets | None):
        """Serialize Targets by unwrapping the value field."""
        if targets is None:
            return None
        return targets.value


class ToJson(BaseModel):
    state: NetworkState
    scan: ScanResults
