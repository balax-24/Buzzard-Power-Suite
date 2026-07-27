"""HP Hardware Vendor Plugin.

Targeted sysfs implementation for HP laptops (Spectre, Envy, OMEN, Pavilion, EliteBook) using
hp-wmi and ACPI platform_profile drivers.
"""

from pathlib import Path
from typing import Any, Dict, List
from buzzard.core.capabilities import Capabilities
from buzzard.core.result import Result
from buzzard.core.shell import Shell
from buzzard.detection import Detection
from buzzard.plugins.base import VendorPlugin


class HPPlugin(VendorPlugin):
    """HP OEM Hardware Plugin."""

    HP_SYSFS = Path("/sys/devices/platform/hp-wmi")
    PLATFORM_PROFILE = Path("/sys/firmware/acpi/platform_profile")

    @property
    def name(self) -> str:
        return "HP WMI Plugin"

    @property
    def vendor_id(self) -> str:
        return "hp"

    def is_compatible(self) -> bool:
        vendor = Detection.vendor().lower()
        return "hp" in vendor or "hewlett" in vendor or self.HP_SYSFS.exists()

    def capabilities(self) -> Capabilities:
        return Capabilities(
            gpu_mux=False,
            battery_limit=Path("/sys/class/power_supply/BAT0/charge_control_end_threshold").exists(),
            fan_curve=False,
            thermal_profiles=self.PLATFORM_PROFILE.exists(),
            refresh_rate_control=True,
            pcie_runtime_pm=True,
            usb_autosuspend=True,
            tlp_support=Shell.exists("tlp"),
            powertop_support=Shell.exists("powertop"),
        )

    def set_battery_charge_limit(self, limit: int) -> Result:
        node = Path("/sys/class/power_supply/BAT0/charge_control_end_threshold")
        if node.exists():
            res = Shell.write_sysfs(node, str(limit))
            if res.success:
                return Result(success=True, message=f"HP battery charge limit set to {limit}%")
        return Result(success=False, message="HP battery charge limit sysfs node not supported")

    def apply_vendor_settings(self, options: Dict[str, Any]) -> List[Result]:
        results: List[Result] = []

        if "battery_charge_limit" in options:
            results.append(self.set_battery_charge_limit(int(options["battery_charge_limit"])))

        if "fan_profile" in options and self.PLATFORM_PROFILE.exists():
            p_map = {"quiet": "quiet", "balanced": "balanced", "performance": "performance", "turbo": "performance"}
            target_profile = p_map.get(str(options["fan_profile"]).lower(), "balanced")
            res = Shell.write_sysfs(self.PLATFORM_PROFILE, target_profile)
            if res.success:
                results.append(Result(success=True, message=f"HP thermal profile set to '{target_profile}'"))

        return results
