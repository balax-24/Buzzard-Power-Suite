"""Buzzard Base Vendor Plugin Interface.

Defines plugin abstract class for OEM-specific hardware capabilities (ASUS, Lenovo, Dell, HP, MSI, Generic).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from buzzard.core.capabilities import Capabilities
from buzzard.core.result import Result


class VendorPlugin(ABC):
    """Abstract Base Class for Hardware Vendor Plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns vendor plugin human-readable name."""
        pass

    @property
    @abstractmethod
    def vendor_id(self) -> str:
        """Returns unique lower-case vendor key (asus, lenovo, dell, hp, msi, framework, generic)."""
        pass

    @abstractmethod
    def is_compatible(self) -> bool:
        """Checks if current host system matches vendor hardware signature."""
        pass

    @abstractmethod
    def capabilities(self) -> Capabilities:
        """Inspects hardware capabilities exposed by host system."""
        pass

    @abstractmethod
    def apply_vendor_settings(self, options: Dict[str, Any]) -> List[Result]:
        """Applies vendor-specific parameters from active profile payload."""
        pass

    def get_battery_charge_limit(self) -> int | None:
        """Gets active battery charging threshold limit percentage if supported."""
        return None

    def set_battery_charge_limit(self, limit: int) -> Result:
        """Sets battery charging threshold limit percentage if supported."""
        return Result(
            success=False,
            message=f"Battery charge threshold not supported on {self.name}",
        )
