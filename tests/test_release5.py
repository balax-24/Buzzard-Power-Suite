"""Unit tests for Release 5 features (DistroDetector, PrivilegeManager, PowerProfilesManager, Setup)."""

from unittest.mock import MagicMock, patch
from buzzard.core.distro import DistroDetector
from buzzard.core.privileges import PrivilegeManager
from buzzard.managers import PowerProfilesManager


def test_distro_detector():
    info = DistroDetector.get_info()
    assert "id" in info
    assert "name" in info

    pm = DistroDetector.get_package_manager()
    assert pm in ["apt", "pacman", "dnf", "zypper", "unknown"]

    pkgs = DistroDetector.get_dependency_packages()
    assert isinstance(pkgs, list)
    assert len(pkgs) > 0


def test_privilege_manager():
    with patch("buzzard.core.shell.Shell.run", return_value=MagicMock(success=True)):
        res = PrivilegeManager.setup_sudoers()
        assert res.success is True


def test_power_profiles_manager():
    with patch("buzzard.core.shell.Shell.exists", return_value=True):
        with patch("buzzard.core.shell.Shell.run", return_value=MagicMock(success=True, stdout="balanced")):
            mode = PowerProfilesManager.get_profile()
            assert mode == "balanced"

            res = PowerProfilesManager.set_profile("low")
            assert res.success is True
