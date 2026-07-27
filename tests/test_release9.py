"""Unit tests for Release 9 features (WorkloadIntrospector & AdaptivePowerService)."""

from unittest.mock import MagicMock, patch
from buzzard.core.workload import WorkloadIntrospector
from buzzard.services.adaptive_service import AdaptivePowerService


def test_workload_introspector_gaming():
    with patch("buzzard.core.workload.WorkloadIntrospector.get_running_processes", return_value="1234 steam /usr/bin/steam"):
        wl = WorkloadIntrospector.detect_workload()
        assert wl == "gaming"


def test_workload_introspector_llm():
    with patch("buzzard.core.workload.WorkloadIntrospector.get_running_processes", return_value="5678 ollama serve"):
        wl = WorkloadIntrospector.detect_workload()
        assert wl == "llm"


def test_adaptive_power_service():
    with patch("buzzard.core.workload.WorkloadIntrospector.detect_workload", return_value="gaming"):
        with patch("buzzard.managers.BatteryManager.is_ac_connected", return_value=True):
            with patch("buzzard.services.profile_service.ProfileService.current", return_value="low"):
                with patch("buzzard.services.profile_service.ProfileService.apply_profile", return_value=(True, [])):
                    changed, target = AdaptivePowerService.evaluate_and_apply(force=True)
                    assert changed is True
                    assert target == "gaming"
