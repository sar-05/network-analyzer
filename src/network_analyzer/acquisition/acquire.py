"""Fucntions to acquire information of targets."""

import logging

from nmapthon2 import NmapScanner

from network_analyzer.utils.scan_models import (
    HostInfo,
    JsonHost,
    OSMatch,
    OSMatchInfo,
    PortInfo,
    ScanResults,
    ServiceInfo,
    Targets,
)

logger = logging.getLogger(__name__)


def acquire(targets: Targets) -> ScanResults | None:
    """Parse nmap scan results of a network into a JSON serializable object."""
    scanner = NmapScanner()
    t = targets.value
    r = scanner.scan(targets=str(t), arguments="--privileged -A --osscan-guess")
    hosts = ScanResults(targets=targets)
    for host in r:
        # Parse host_info
        host_info = HostInfo(
            address=host.ipv4,
            hostname=host.hostnames() or None,
            state=host.state,
            reason=host.reason,
            scan_time=f"{host.start_time}",
        )

        # Parse os_info
        os_info = host.most_accurate_os()
        name = os_info.name
        accuracy = os_info.accuracy

        info_dict: dict[int, OSMatchInfo] = {}
        for i, match in enumerate(os_info.get_matches()):
            info_dict[i + 1] = OSMatchInfo(
                type=match.type,
                vendor=match.vendor,
                family=match.family,
            )

        best_match = OSMatch(name=name, accuracy=accuracy, info=info_dict)

        # Parse ports
        ports: dict[int, PortInfo] = {}
        for p in host:
            svc = p.service
            svc_info = None
            if svc:
                svc_info = ServiceInfo(
                    name=svc.name,
                    product=svc.product,
                    version=svc.version,
                    confidence=svc.conf,
                    extrainfo=svc.extrainfo,
                )
            ports[p.number] = PortInfo(
                port=p.number,
                protocol=p.protocol,
                state=p.state,
                reason=p.reason,
                service=svc_info,
            )

        hosts[host.ipv4] = JsonHost(
            host_info=host_info,
            best_match=best_match,
            ports=ports,
        )

    return hosts
