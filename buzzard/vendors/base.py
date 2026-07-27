"""Base abstract vendor class for hardware-specific power and diagnostic extensions.

All vendor backends (ASUS, Lenovo, Dell, HP, Generic) inherit from VendorBackend
to provide hardware control such as battery charge limits, GPU MUX switches,
and thermal profiles.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from buzzard.core.result import Result


class VendorBackend(ABC):
    """Abstract Base Class for Vendor Backend Implementations."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns human-readable name of vendor backend."""
        pass

    @abstractmethod
    def detect(self) -> bool:
        """Detects if current machine matches this vendor hardware.

        Returns:
            True if hardware matches vendor backend, False otherwise.
        """
        pass

    @abstractmethod
    def capabilities(self) -> Dict[str, bool]:
        """Returns dictionary of supported vendor features on this hardware.

        Returns:
            Dict mapping feature name to availability boolean.
        """
        pass

    @abstractmethod
    def apply_vendor_settings(self, options: Dict[str, Any]) -> List[Result]:
        """Applies vendor-specific options from profile configuration.

        Args:
            options: Vendor settings dictionary from profile.

        Returns:
            List of Result objects.
        """
        pass

    @abstractmethod
    def get_battery_charge_limit(self) -> int | None:
        """Gets current battery charge threshold limit if supported.

        Returns:
            Integer percentage limit (e.g. 80, 100) or None if unsupported.
        """
        pass

    @abstractmethod
    def set_battery_charge_limit(self, limit: int) -> Result:
        """Sets battery charge threshold limit.

        Args:
            limit: Charge limit percentage (e.g. 60, 80, 100).

        Returns:
            Result object.
        """
        pass
