"""Vendor Hardware Extension Manager.

Delegates hardware-specific OEM controls to active VendorPlugin.
"""

from typing import Any, Dict, List
from buzzard.core.capabilities import Capabilities
from buzzard.core.result import Result
from buzzard.plugins.manager import PluginManager


class VendorManager:
    """Vendor Hardware Subsystem Manager using Plugin Architecture."""

    @classmethod
    def get_plugin(cls):
        """Retrieves active vendor plugin instance.

        Returns:
            VendorPlugin subclass instance.
        """
        return PluginManager.get_active_plugin()

    @classmethod
    def vendor_name(cls) -> str:
        """Returns detected vendor plugin name.

        Returns:
            Vendor name string.
        """
        return cls.get_plugin().name

    @classmethod
    def capabilities(cls) -> Capabilities:
        """Returns vendor hardware capabilities object.

        Returns:
            Capabilities instance.
        """
        return cls.get_plugin().capabilities()

    @classmethod
    def apply_vendor_settings(cls, options: Dict[str, Any]) -> List[Result]:
        """Applies vendor-specific options from active profile payload.

        Args:
            options: Options dictionary from profile.

        Returns:
            List of Result objects.
        """
        return cls.get_plugin().apply_vendor_settings(options)

    @classmethod
    def get_charge_limit(cls) -> int | None:
        """Gets active battery charge threshold limit.

        Returns:
            Limit percentage or None.
        """
        return cls.get_plugin().get_battery_charge_limit()

    @classmethod
    def set_charge_limit(cls, limit: int) -> Result:
        """Sets battery charge threshold limit.

        Args:
            limit: Charge limit percentage.

        Returns:
            Result object.
        """
        return cls.get_plugin().set_battery_charge_limit(limit)
