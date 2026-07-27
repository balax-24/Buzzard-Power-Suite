"""Framework Laptop Hardware Vendor Plugin.

Targeted sysfs / ECTool implementation for Framework 13 & 16 laptops.
"""

from pathlib import Path
from typing import Any, Dict, List
from buzzard.core.capabilities import Capabilities
from buzzard.core.result import Result
from buzzard.core.shell import Shell
from buzzard.detection import Detection
from buzzard.plugins.base import VendorPlugin


class FrameworkPlugin(VendorPlugin):
    """Framework Laptop OEM Plugin."""

    PLATFORM_PROFILE = Path("/sys/firmware/acpi/platform_profile")
    BAT0_LIMIT = Path("/sys/class/power_supply/BAT0/charge_control_end_threshold")

    @property
    def name(self) -> str:
        return "Framework Laptop Plugin"

    @property
    def vendor_id(self) -> str:
        return "framework"

    def is_compatible(self) -> bool:
        vendor = Detection.vendor().lower()
        return "framework" in vendor

    def capabilities(self) -> Capabilities:
        return Capabilities(
            gpu_mux=False,
            battery_limit=self.BAT0_LIMIT.exists(),
            fan_curve=False,
            thermal_profiles=self.PLATFORM_PROFILE.exists(),
            refresh_rate_control=True,
            pcie_runtime_pm=True,
            usb_autosuspend=True,
            tlp_support=Shell.exists("tlp"),
            powertop_support=Shell.exists("powertop"),
        )

    def set_battery_charge_limit(self, limit: int) -> Result:
        if self.BAT0_LIMIT.exists():
            res = Shell.write_sysfs(self.BAT0_LIMIT, str(limit))
            if res.success:
                return Result(success=True, message=f"Framework battery charge limit set to {limit}%")
        return Result(success=False, message="Framework battery limit node not supported")

    def apply_vendor_settings(self, options: Dict[str, Any]) -> List[Result]:
        results: List[Result] = []

        if "battery_charge_limit" in options:
            results.append(self.set_battery_charge_limit(int(options["battery_charge_limit"])))

        if "fan_profile" in options and self.PLATFORM_PROFILE.exists():
            p_map = {"quiet": "low-power", "balanced": "balanced", "performance": "performance"}
            target_profile = p_map.get(str(options["fan_profile"]).lower(), "balanced")
            res = Shell.write_sysfs(self.PLATFORM_PROFILE, target_profile)
            if res.success:
                results.append(Result(success=True, message=f"Framework thermal profile set to '{target_profile}'"))

        return results
