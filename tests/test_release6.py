"""Unit tests for Release 6 features (MacMode, KernelPowerManager, EPP, Turbo Boost)."""

from unittest.mock import MagicMock, patch
from buzzard.managers import CPUManager, KernelPowerManager, MacModeManager


def test_cpu_turbo_and_epp():
    with patch("buzzard.core.shell.Shell.write_sysfs", return_value=MagicMock(success=True)):
        res_tb = CPUManager.set_turbo_boost(False)
        assert res_tb.success is True

    with patch("buzzard.core.shell.Shell.run", return_value=MagicMock(success=True)):
        res_epp = CPUManager.set_epp("power")
        assert res_epp.success is True


def test_kernel_power_manager():
    with patch("buzzard.core.shell.Shell.write_sysfs", return_value=MagicMock(success=True)):
        with patch("buzzard.core.shell.Shell.exists", return_value=False):
            results = KernelPowerManager.apply_ultra_power_save()
            assert isinstance(results, list)


def test_macmode_manager():
    with patch("buzzard.managers.GPUManager.use_intel", return_value=MagicMock(success=True)):
        with patch("buzzard.managers.CPUManager.powersave", return_value=MagicMock(success=True)):
            with patch("buzzard.managers.CPUManager.set_epp", return_value=MagicMock(success=True)):
                with patch("buzzard.managers.CPUManager.set_turbo_boost", return_value=MagicMock(success=True)):
                    with patch("buzzard.managers.DisplayManager.set_refresh_rate", return_value=MagicMock(success=True)):
                        with patch("buzzard.managers.BrightnessManager.set", return_value=MagicMock(success=True)):
                            with patch("buzzard.managers.BluetoothManager.disable", return_value=MagicMock(success=True)):
                                with patch("buzzard.managers.PCIeManager.enable_powersave", return_value=MagicMock(success=True)):
                                    with patch("buzzard.managers.KernelPowerManager.apply_ultra_power_save", return_value=[]):
                                        with patch("buzzard.managers.TLPManager.start", return_value=MagicMock(success=True)):
                                            with patch("buzzard.managers.PowerTOPManager.autotune", return_value=MagicMock(success=True)):
                                                res_list = MacModeManager.activate_macmode()
                                                assert len(res_list) >= 10
