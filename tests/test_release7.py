"""Unit tests for Release 7 features (Wi-Fi Throttle Prevention & System Tray GUI)."""

from unittest.mock import MagicMock, patch
from buzzard.managers import KernelPowerManager


def test_wifi_power_save_kept_off():
    with patch("buzzard.core.shell.Shell.write_sysfs", return_value=MagicMock(success=True)):
        with patch("buzzard.core.shell.Shell.exists", return_value=True):
            with patch("buzzard.core.shell.Shell.run", return_value=MagicMock(success=True, stdout="Interface wlo1\n")):
                results = KernelPowerManager.apply_ultra_power_save()
                wifi_res = [r for r in results if "Wi-Fi" in r.message]
                assert len(wifi_res) > 0
                assert "power save OFF" in wifi_res[0].message
