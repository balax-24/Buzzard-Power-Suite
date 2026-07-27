"""Unit tests for Release 4 features (EventBus, Capabilities, Plugins, Display, Estimator, Daemon)."""

from unittest.mock import MagicMock, patch
from buzzard.core.capabilities import Capabilities
from buzzard.core.event_bus import EventBus, ProfileAppliedEvent
from buzzard.core.state_machine import ProfileState, ProfileStateMachine
from buzzard.managers import DisplayManager, PCIeManager, PowerEstimator
from buzzard.plugins.asus import ASUSPlugin
from buzzard.plugins.lenovo import LenovoPlugin
from buzzard.plugins.manager import PluginManager
from buzzard.services import DaemonService, NotificationService


def test_capabilities_model():
    caps = Capabilities(gpu_mux=True, battery_limit=True)
    d = caps.to_dict()
    assert d["gpu_mux"] is True
    assert d["battery_limit"] is True
    assert d["fan_curve"] is False


def test_event_bus():
    received = []

    def handler(evt: ProfileAppliedEvent):
        received.append(evt.profile_name)

    EventBus.subscribe(ProfileAppliedEvent, handler)
    EventBus.publish(ProfileAppliedEvent(profile_name="gaming"))
    assert received == ["gaming"]
    EventBus.clear()


def test_state_machine():
    sm = ProfileStateMachine("full")
    assert sm.state == ProfileState.IDLE
    sm.transition_to(ProfileState.APPLYING)
    assert sm.state == ProfileState.APPLYING
    sm.transition_to(ProfileState.COMPLETED)
    assert sm.is_terminal() is True


def test_plugin_discovery():
    plugin = PluginManager.get_active_plugin()
    assert plugin.vendor_id in ["asus", "lenovo", "dell", "generic"]


def test_power_estimator():
    with patch("buzzard.managers.BatteryManager.health_report") as mock_bat:
        mock_bat.return_value = {
            "power_draw_w": 10.0,
            "capacity_percent": 80,
            "status": "Discharging",
            "ac_connected": False,
        }
        est = PowerEstimator.estimate()
        assert est["status"] == "Discharging"
        assert est["power_draw_w"] == 10.0
        assert "h " in est["estimated_runtime"]


def test_display_manager():
    with patch("buzzard.core.shell.Shell.exists", return_value=True):
        with patch("buzzard.core.shell.Shell.run") as mock_run:
            mock_run.side_effect = [
                MagicMock(success=True, stdout="eDP-1 connected 1920x1080", stderr="", code=0),
                MagicMock(success=True, stdout="Set 120Hz", stderr="", code=0),
            ]
            res = DisplayManager.set_refresh_rate(120)
            assert res.success is True


def test_pcie_manager():
    res = PCIeManager.enable_powersave()
    assert res.success is True


def test_daemon_service_install(tmp_path):
    with patch("buzzard.services.daemon_service.DaemonService.SYSTEMD_USER_DIR", tmp_path):
        with patch("buzzard.services.daemon_service.DaemonService.SERVICE_FILE", tmp_path / "service"):
            with patch("buzzard.core.shell.Shell.run", return_value=MagicMock(success=True)):
                res = DaemonService.install_systemd_service()
                assert res.success is True
