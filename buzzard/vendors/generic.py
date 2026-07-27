"""Generic Linux Vendor Backend.

Fallback vendor backend for standard Linux systems without vendor-specific WMI
or sysfs extensions.
"""

from typing import Any, Dict, List
from buzzard.core.result import Result
from buzzard.vendors.base import VendorBackend


class GenericVendor(VendorBackend):
    """Generic Linux Hardware Vendor Backend."""

    @property
    def name(self) -> str:
        return "Generic Linux"

    def detect(self) -> bool:
        return True

    def capabilities(self) -> Dict[str, bool]:
        return {
            "battery_charge_limit": False,
            "gpu_mux": False,
            "fan_profiles": False,
        }

    def apply_vendor_settings(self, options: Dict[str, Any]) -> List[Result]:
        return []

    def get_battery_charge_limit(self) -> int | None:
        return None

    def set_battery_charge_limit(self, limit: int) -> Result:
        return Result(
            success=False,
            message="Battery charge limiting is not supported on generic vendor backend",
        )
