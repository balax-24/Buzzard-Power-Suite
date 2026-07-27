"""Unit tests for Buzzard Core layer (Result and Shell execution wrapper)."""

from unittest.mock import MagicMock, patch
from buzzard.core.result import Result
from buzzard.core.shell import Shell, ShellResult


def test_result_defaults():
    res = Result(success=True, message="Operation successful")
    assert res.success is True
    assert res.message == "Operation successful"
    assert res.stdout == ""
    assert res.stderr == ""
    assert res.reboot_required is False
    assert res.rollback_available is False
    assert res.to_dict()["success"] is True


def test_shell_run_success():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="output_text\n", stderr="")
        res = Shell.run("echo hello")
        assert res.success is True
        assert res.stdout == "output_text"
        assert res.code == 0


def test_shell_run_failure():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="command failed\n")
        res = Shell.run("false")
        assert res.success is False
        assert res.stderr == "command failed"
        assert res.code == 1


def test_shell_exists():
    assert Shell.exists("python3") is True
    assert Shell.exists("non_existent_binary_buzzard_123") is False
