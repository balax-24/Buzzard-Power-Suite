"""Generic Linux Hardware Vendor Plugin.

Default fallback hardware plugin for Linux laptops and desktop machines.
"""

from typing import Any, Dict, List
from buzzard.core.capabilities import Capabilities
from buzzard.core.result import Result
from buzzard.core.shell import Shell
from buzzard.plugins.base import VendorPlugin


class GenericPlugin(VendorPlugin):
    """Generic Linux Plugin."""

    @property
    def name(self) -> str:
        return "Generic Linux Backend"

    @property
    def vendor_id(self) -> str:
        return "generic"

    def is_compatible(self) -> bool:
        return True

    def capabilities(self) -> Capabilities:
        return Capabilities(
            gpu_mux=False,
            battery_limit=False,
            fan_curve=False,
            thermal_profiles=False,
            refresh_rate_control=True,
            pcie_runtime_pm=True,
            usb_autosuspend=True,
            tlp_support=Shell.exists("tlp"),
            powertop_support=Shell.exists("powertop"),
        )

    def apply_vendor_settings(self, options: Dict[str, Any]) -> List[Result]:
        return []
