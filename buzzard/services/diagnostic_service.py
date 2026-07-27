"""Buzzard Health & Diagnostic Service.

Provides hardware detection, dependency availability checks, sysfs node inspection,
and system doctor diagnostic reports.
"""

from typing import Any, Dict
from buzzard.dependencies import Dependencies
from buzzard.detection import Detection
from buzzard.managers import BatteryManager, PowerTOPManager, TLPManager, VendorManager


class DiagnosticService:
    """Service for system health diagnostics and dependency verification."""

    @classmethod
    def report(cls) -> Dict[str, Any]:
        """Generates comprehensive system doctor report.

        Returns:
            Dictionary containing hardware detection, kernel details, dependencies, and vendor info.
        """
        deps = Dependencies.check()
        bat = BatteryManager.health_report()
        vendor = VendorManager.vendor_name()
        caps = VendorManager.capabilities()
        caps_dict = caps.to_dict() if hasattr(caps, "to_dict") else dict(caps)

        missing_deps = [dep for dep, ok in deps.items() if not ok]

        return {
            "vendor": Detection.vendor(),
            "product": Detection.product(),
            "bios": Detection.bios(),
            "kernel": Detection.kernel(),
            "architecture": Detection.architecture(),
            "hostname": Detection.hostname(),
            "vendor_backend": vendor,
            "vendor_capabilities": caps_dict,
            "dependencies": deps,
            "missing_dependencies": missing_deps,
            "tlp_installed": TLPManager.is_installed(),
            "powertop_installed": PowerTOPManager.is_installed(),
            "battery_health": bat,
            "is_healthy": len(missing_deps) == 0,
        }
