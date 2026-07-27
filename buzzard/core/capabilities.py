"""Buzzard System Capabilities Engine.

Defines feature flag capabilities model for vendor and hardware hardware inspection.
"""

from dataclasses import asdict, dataclass
from typing import Dict


@dataclass
class Capabilities:
    """Hardware Feature Flag Capabilities Dataclass."""

    gpu_mux: bool = False
    battery_limit: bool = False
    fan_curve: bool = False
    thermal_profiles: bool = False
    refresh_rate_control: bool = False
    pcie_runtime_pm: bool = False
    usb_autosuspend: bool = False
    tlp_support: bool = False
    powertop_support: bool = False

    def to_dict(self) -> Dict[str, bool]:
        """Converts capabilities model to dictionary.

        Returns:
            Dict of feature name to boolean status.
        """
        return asdict(self)
