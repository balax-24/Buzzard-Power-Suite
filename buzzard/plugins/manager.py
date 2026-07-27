"""Plugin Registry Manager for Vendor HW Plugins."""

from typing import List, Optional
from buzzard.plugins.asus import ASUSPlugin
from buzzard.plugins.base import VendorPlugin
from buzzard.plugins.dell import DellPlugin
from buzzard.plugins.framework import FrameworkPlugin
from buzzard.plugins.generic import GenericPlugin
from buzzard.plugins.hp import HPPlugin
from buzzard.plugins.lenovo import LenovoPlugin


class PluginManager:
    """Discovers, loads, and manages vendor-specific hardware plugins."""

    _PLUGINS: List[VendorPlugin] = [
        ASUSPlugin(),
        LenovoPlugin(),
        DellPlugin(),
        HPPlugin(),
        FrameworkPlugin(),
        GenericPlugin(),
    ]

    @classmethod
    def get_active_plugin(cls) -> VendorPlugin:
        """Finds first matching compatible vendor plugin or falls back to GenericPlugin.

        Returns:
            Compatible VendorPlugin instance.
        """
        for plugin in cls._PLUGINS:
            try:
                if plugin.is_compatible():
                    return plugin
            except Exception:
                continue
        return GenericPlugin()

    @classmethod
    def active_vendor_id(cls) -> str:
        """Returns vendor ID string of active compatible plugin.

        Returns:
            Vendor ID string (asus, lenovo, dell, hp, framework, generic).
        """
        return cls.get_active_plugin().vendor_id

    @classmethod
    def get_plugin_by_id(cls, vendor_id: str) -> Optional[VendorPlugin]:
        """Gets plugin instance by vendor ID string.

        Args:
            vendor_id: Identifier string (asus, lenovo, dell, hp, framework, generic).

        Returns:
            Plugin instance or None.
        """
        vendor_id = vendor_id.lower().strip()
        for plugin in cls._PLUGINS:
            if plugin.vendor_id == vendor_id:
                return plugin
        return None
