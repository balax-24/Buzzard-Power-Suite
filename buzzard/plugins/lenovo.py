"""Lenovo Hardware Vendor Plugin.

Targeted sysfs implementation for Lenovo laptops (IdeaPad, ThinkPad, Legion) using
ideapad_laptop / thinkpad_acpi drivers.
"""

from pathlib import Path
from typing import Any, Dict, List
from buzzard.core.capabilities import Capabilities
from buzzard.core.result import Result
from buzzard.core.shell import Shell
from buzzard.detection import Detection
from buzzard.plugins.base import VendorPlugin


class LenovoPlugin(VendorPlugin):
    """Lenovo OEM Hardware Plugin."""

    IDEAPAD_SYSFS = Path("/sys/bus/platform/drivers/ideapad_laptop")
    THINKPAD_SYSFS = Path("/sys/devices/platform/thinkpad_acpi")

    @property
    def name(self) -> str:
        return "Lenovo ACPI Plugin"

    @property
    def vendor_id(self) -> str:
        return "lenovo"

    def is_compatible(self) -> bool:
        vendor = Detection.vendor().lower()
        return "lenovo" in vendor or self.IDEAPAD_SYSFS.exists() or self.THINKPAD_SYSFS.exists()

    def capabilities(self) -> Capabilities:
        cons_node = Path("/sys/bus/platform/drivers/ideapad_laptop/VPC2004:00/conservation_mode")
        return Capabilities(
            gpu_mux=False,
            battery_limit=cons_node.exists(),
            fan_curve=False,
            thermal_profiles=True,
            refresh_rate_control=True,
            pcie_runtime_pm=True,
            usb_autosuspend=True,
            tlp_support=Shell.exists("tlp"),
            powertop_support=Shell.exists("powertop"),
        )

    def get_battery_charge_limit(self) -> int | None:
        cons_node = Path("/sys/bus/platform/drivers/ideapad_laptop/VPC2004:00/conservation_mode")
        val = Shell.read_sysfs(cons_node)
        if val == "1":
            return 60
        if val == "0":
            return 100
        return None

    def set_battery_charge_limit(self, limit: int) -> Result:
        cons_node = Path("/sys/bus/platform/drivers/ideapad_laptop/VPC2004:00/conservation_mode")
        if cons_node.exists():
            val = "1" if limit <= 80 else "0"
            res = Shell.write_sysfs(cons_node, val)
            if res.success:
                return Result(
                    success=True,
                    message=f"Lenovo Conservation Mode set to {val} (Limit: {limit}%)",
                    rollback_available=True,
                )

        return Result(
            success=False,
            message="Lenovo Conservation Mode sysfs node not found",
        )

    def apply_vendor_settings(self, options: Dict[str, Any]) -> List[Result]:
        results: List[Result] = []
        if "battery_charge_limit" in options:
            results.append(self.set_battery_charge_limit(int(options["battery_charge_limit"])))
        return results
