"""Unit tests for Hardware Subsystem Managers."""

from unittest.mock import MagicMock, patch
from buzzard.core.result import Result
from buzzard.managers import (
    BatteryManager,
    BluetoothManager,
    BrightnessManager,
    CPUManager,
    GPUManager,
    PowerTOPManager,
    TLPManager,
    VendorManager,
)


def test_cpu_manager_current():
    with patch("buzzard.core.shell.Shell.read_sysfs", return_value="powersave"):
        assert CPUManager.current() == "powersave"


def test_cpu_manager_set_governor():
    with patch("buzzard.managers.cpu.CPUManager.current", return_value="performance"):
        with patch("buzzard.core.shell.Shell.run") as mock_run:
            mock_run.return_value = MagicMock(success=True, stdout="", stderr="", code=0)
            res = CPUManager.powersave()
            assert isinstance(res, Result)
            assert res.success is True
            assert "powersave" in res.message


def test_gpu_manager_intel():
    with patch("buzzard.managers.gpu.GPUManager.current", return_value="nvidia"):
        with patch("buzzard.core.shell.Shell.exists", return_value=True):
            with patch("buzzard.core.shell.Shell.run") as mock_run:
                mock_run.return_value = MagicMock(success=True, stdout="Switched", stderr="", code=0)
                res = GPUManager.use_intel()
                assert res.success is True
                assert res.reboot_required is True


def test_brightness_manager():
    with patch("buzzard.core.shell.Shell.exists", return_value=True):
        with patch("buzzard.core.shell.Shell.run") as mock_run:
            mock_run.return_value = MagicMock(success=True, stdout="50", stderr="", code=0)
            val = BrightnessManager.get()
            assert isinstance(val, int)


def test_bluetooth_manager():
    with patch("buzzard.managers.bluetooth.BluetoothManager.status", return_value="Enabled"):
        with patch("buzzard.core.shell.Shell.exists", return_value=True):
            with patch("buzzard.core.shell.Shell.run") as mock_run:
                mock_run.return_value = MagicMock(success=True, stdout="", stderr="", code=0)
                res = BluetoothManager.disable()
                assert res.success is True


def test_powertop_manager():
    with patch("buzzard.core.shell.Shell.exists", return_value=True):
        with patch("buzzard.core.shell.Shell.run") as mock_run:
            mock_run.return_value = MagicMock(success=True, stdout="Autotuned", stderr="", code=0)
            res = PowerTOPManager.autotune()
            assert res.success is True
