"""Integration and unit tests for Service Layer."""

from unittest.mock import MagicMock, patch
from buzzard.core.result import Result
from buzzard.services import (
    DiagnosticService,
    HistoryService,
    OptimizeService,
    ProfileService,
    RestoreService,
    StatusService,
)


def test_status_service():
    with patch("buzzard.managers.GPUManager.current", return_value="intel"):
        with patch("buzzard.managers.CPUManager.current", return_value="powersave"):
            status = StatusService.get_status()
            assert status["gpu"] == "intel"
            assert status["cpu_governor"] == "powersave"


def test_diagnostic_service():
    report = DiagnosticService.report()
    assert "vendor" in report
    assert "kernel" in report
    assert "dependencies" in report


def test_profile_service_apply(tmp_path):
    with patch("buzzard.services.profile_service.CURRENT_PROFILE_FILE", tmp_path / "curr"):
        with patch("buzzard.services.profile_service.PREVIOUS_PROFILE_FILE", tmp_path / "prev"):
            with patch("buzzard.managers.GPUManager.use_intel", return_value=Result(success=True, message="OK")):
                with patch("buzzard.managers.CPUManager.set_governor", return_value=Result(success=True, message="OK")):
                    with patch("buzzard.managers.BrightnessManager.set", return_value=Result(success=True, message="OK")):
                        with patch("buzzard.managers.BluetoothManager.disable", return_value=Result(success=True, message="OK")):
                            with patch("buzzard.managers.TLPManager.start", return_value=Result(success=True, message="OK")):
                                success, results = ProfileService.apply_profile("low")
                                assert success is True
                                assert ProfileService.current() == "low"


def test_history_service(tmp_path):
    with patch("buzzard.services.history_service.HISTORY_FILE", tmp_path / "history.json"):
        with patch("buzzard.services.history_service.DATA_DIR", tmp_path):
            HistoryService.record(
                profile="hybrid",
                duration=0.5,
                status="SUCCESS",
                battery=85,
                cpu_governor="powersave",
                gpu="hybrid",
            )
            records = HistoryService.get_history()
            assert len(records) == 1
            assert records[0]["profile"] == "hybrid"
