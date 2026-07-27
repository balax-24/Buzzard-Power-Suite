"""ASUS Hardware Vendor Plugin.

Targeted WMI/sysfs implementation for ASUS laptops (Vivobook, ROG, TUF, ZenBook).
"""

from pathlib import Path
from typing import Any, Dict, List
from buzzard.core.capabilities import Capabilities
from buzzard.core.result import Result
from buzzard.core.shell import Shell
from buzzard.detection import Detection
from buzzard.plugins.base import VendorPlugin


class ASUSPlugin(VendorPlugin):
    """ASUS OEM Hardware Plugin."""

    ASUS_SYSFS = Path("/sys/devices/platform/asus-nb-wmi")

    @property
    def name(self) -> str:
        return "ASUS WMI Plugin"

    @property
    def vendor_id(self) -> str:
        return "asus"

    def is_compatible(self) -> bool:
        vendor = Detection.vendor().lower()
        return "asus" in vendor or self.ASUS_SYSFS.exists()

    def capabilities(self) -> Capabilities:
        return Capabilities(
            gpu_mux=(self.ASUS_SYSFS / "gpu_mux").exists(),
            battery_limit=(self.ASUS_SYSFS / "charge_control_end_threshold").exists()
            or Path("/sys/class/power_supply/BAT0/charge_control_end_threshold").exists(),
            fan_curve=(self.ASUS_SYSFS / "throttle_thermal_policy").exists(),
            thermal_profiles=(self.ASUS_SYSFS / "throttle_thermal_policy").exists(),
            refresh_rate_control=True,
            pcie_runtime_pm=True,
            usb_autosuspend=True,
            tlp_support=Shell.exists("tlp"),
            powertop_support=Shell.exists("powertop"),
        )

    def get_battery_charge_limit(self) -> int | None:
        nodes = [
            self.ASUS_SYSFS / "charge_control_end_threshold",
            Path("/sys/class/power_supply/BAT0/charge_control_end_threshold"),
            Path("/sys/class/power_supply/BAT1/charge_control_end_threshold"),
        ]
        for node in nodes:
            val = Shell.read_sysfs(node)
            if val.isdigit():
                return int(val)
        return None

    def set_battery_charge_limit(self, limit: int) -> Result:
        limit = max(40, min(100, limit))
        nodes = [
            self.ASUS_SYSFS / "charge_control_end_threshold",
            Path("/sys/class/power_supply/BAT0/charge_control_end_threshold"),
            Path("/sys/class/power_supply/BAT1/charge_control_end_threshold"),
        ]

        for node in nodes:
            if node.exists():
                res = Shell.write_sysfs(node, str(limit))
                if res.success:
                    return Result(
                        success=True,
                        message=f"ASUS battery charge limit set to {limit}%",
                        rollback_available=True,
                    )

        return Result(
            success=False,
            message="ASUS battery charge limit sysfs node not writable",
        )

    def apply_vendor_settings(self, options: Dict[str, Any]) -> List[Result]:
        results: List[Result] = []

        # 1. Battery charge limit
        if "battery_charge_limit" in options:
            results.append(self.set_battery_charge_limit(int(options["battery_charge_limit"])))

        # 2. Thermal Policy / Fan Profile (0: Normal, 1: Boost, 2: Silent)
        if "fan_profile" in options:
            policy_map = {"quiet": 2, "balanced": 0, "performance": 0, "turbo": 1}
            policy_val = policy_map.get(str(options["fan_profile"]).lower(), 0)
            thermal_node = self.ASUS_SYSFS / "throttle_thermal_policy"

            if thermal_node.exists():
                res = Shell.write_sysfs(thermal_node, str(policy_val))
                if res.success:
                    results.append(
                        Result(
                            success=True,
                            message=f"ASUS fan profile set to '{options['fan_profile']}'",
                        )
                    )
                else:
                    results.append(
                        Result(
                            success=False,
                            message=f"Failed setting ASUS fan profile: {res.stderr}",
                        )
                    )

        return results
