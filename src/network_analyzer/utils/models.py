from ipaddress import IPv4Address, IPv6Address

from pydantic import BaseModel, Field


class ServiceInfo(BaseModel):
    name: str | None = None
    product: str | None = None
    version: str | None = None
    confidence: int | None = None
    extrainfo: str | None = None


class PortInfo(BaseModel):
    port: int
    protocol: str
    state: str
    reason: str | None = None
    service: ServiceInfo | None = None


class OSMatchInfo(BaseModel):
    type: str | None
    vendor: str | None
    family: str | None
    # cpe: list[str] | None = None


class OSMatch(BaseModel):
    name: str | None
    accuracy: int | None
    info: dict[int, OSMatchInfo]


class HostInfo(BaseModel):
    address: IPv4Address | IPv6Address
    hostname: list[str] | None = None
    state: str
    reason: str | None = None
    scan_time: str | None = None


class JsonHost(BaseModel):
    host_info: HostInfo
    best_match: OSMatch | None = None
    # os_matches: dict[int, OSMatch] | None = None
    ports: dict[int, PortInfo] = Field(default_factory=dict)


class ScanResults(BaseModel):
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
