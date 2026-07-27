"""Unit tests for Release 8 features (Multi-Vendor OEM Plugins: ASUS, Lenovo, Dell, HP, Framework)."""

from unittest.mock import MagicMock, patch
from buzzard.plugins.dell import DellPlugin
from buzzard.plugins.framework import FrameworkPlugin
from buzzard.plugins.hp import HPPlugin
from buzzard.plugins.manager import PluginManager


def test_plugin_discovery_release8():
    assert PluginManager.get_plugin_by_id("asus") is not None
    assert PluginManager.get_plugin_by_id("lenovo") is not None
    assert PluginManager.get_plugin_by_id("dell") is not None
    assert PluginManager.get_plugin_by_id("hp") is not None
    assert PluginManager.get_plugin_by_id("framework") is not None


def test_dell_plugin():
    dell = DellPlugin()
    assert dell.vendor_id == "dell"
    with patch("buzzard.core.shell.Shell.write_sysfs", return_value=MagicMock(success=True)):
        results = dell.apply_vendor_settings({"battery_charge_limit": 80})
        assert len(results) == 1


def test_hp_plugin():
    hp = HPPlugin()
    assert hp.vendor_id == "hp"
    with patch("buzzard.core.shell.Shell.write_sysfs", return_value=MagicMock(success=True)):
        results = hp.apply_vendor_settings({"battery_charge_limit": 80})
        assert len(results) == 1


def test_framework_plugin():
    fw = FrameworkPlugin()
    assert fw.vendor_id == "framework"
    with patch("buzzard.core.shell.Shell.write_sysfs", return_value=MagicMock(success=True)):
        results = fw.apply_vendor_settings({"battery_charge_limit": 80})
        assert len(results) == 1
