"""ASUS Vendor Backend.

Hardware control backend for ASUS laptops (Vivobook, ROG, TUF, Zenbook).
Supports battery charge limiting, thermal throttle policy, and dGPU WMI control.
"""

from pathlib import Path
from typing import Any, Dict, List
from buzzard.core.result import Result
from buzzard.core.shell import Shell
from buzzard.detection import Detection
from buzzard.vendors.base import VendorBackend


class ASUSVendor(VendorBackend):
    """ASUS WMI & Sysfs Power Backend."""

    CHARGE_LIMIT_PATHS = [
        Path("/sys/class/power_supply/BAT0/charge_control_end_threshold"),
        Path("/sys/class/power_supply/BAT1/charge_control_end_threshold"),
    ]

    THERMAL_POLICY_PATH = Path("/sys/devices/platform/asus-nb-wmi/throttle_thermal_policy")
    DGPU_DISABLE_PATH = Path("/sys/devices/platform/asus-nb-wmi/dgpu_disable")

    @property
    def name(self) -> str:
        return "ASUS WMI Backend"

    def detect(self) -> bool:
        vendor = Detection.vendor().lower()
        return "asus" in vendor or "asustek" in vendor

    def capabilities(self) -> Dict[str, bool]:
        return {
            "battery_charge_limit": self._get_charge_limit_path() is not None,
            "fan_profiles": self.THERMAL_POLICY_PATH.exists(),
            "dgpu_disable": self.DGPU_DISABLE_PATH.exists(),
        }

    def _get_charge_limit_path(self) -> Path | None:
        for p in self.CHARGE_LIMIT_PATHS:
            if p.exists():
                return p
        return None

    def get_battery_charge_limit(self) -> int | None:
        p = self._get_charge_limit_path()
        if p:
            val = Shell.read_sysfs(p)
            if val.isdigit():
                return int(val)
        return None

    def set_battery_charge_limit(self, limit: int) -> Result:
        p = self._get_charge_limit_path()
        if not p:
            return Result(
                success=False,
                message="ASUS battery charge limit sysfs node not found",
            )

        limit = max(60, min(100, limit))
        res = Shell.write_sysfs(p, str(limit))
        if res.success:
            return Result(
                success=True,
                message=f"ASUS battery charge limit set to {limit}%",
            )
        return Result(
            success=False,
            message=f"Failed to set ASUS charge limit: {res.stderr}",
            stderr=res.stderr,
        )

    def set_thermal_policy(self, mode: str) -> Result:
        if not self.THERMAL_POLICY_PATH.exists():
            return Result(
                success=False,
                message="ASUS thermal policy sysfs node unavailable",
            )
        
        # 0: Standard/Balanced, 1: Performance/Turbo, 2: Quiet/Silent
        val_map = {"powersave": "2", "quiet": "2", "balanced": "0", "performance": "1", "turbo": "1"}
        val = val_map.get(mode.lower(), "0")
        res = Shell.write_sysfs(self.THERMAL_POLICY_PATH, val)
        if res.success:
            return Result(
                success=True,
                message=f"ASUS thermal policy set to {mode} (code {val})",
            )
        return Result(
            success=False,
            message=f"Failed setting thermal policy: {res.stderr}",
            stderr=res.stderr,
        )

    def apply_vendor_settings(self, options: Dict[str, Any]) -> List[Result]:
        results = []
        if "charge_limit" in options and self.capabilities()["battery_charge_limit"]:
            results.append(self.set_battery_charge_limit(int(options["charge_limit"])))

        if "thermal_policy" in options and self.capabilities()["fan_profiles"]:
            results.append(self.set_thermal_policy(str(options["thermal_policy"])))

        return results
