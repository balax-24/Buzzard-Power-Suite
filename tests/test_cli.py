"""Smoke tests for CLI command execution via Dispatcher."""

from buzzard.dispatcher import dispatch


def test_cli_help(capsys):
    dispatch(["help"])
    captured = capsys.readouterr()
    assert "Buzzard Power Suite" in captured.out
    assert "USAGE:" in captured.out


def test_cli_version(capsys):
    dispatch(["version"])
    captured = capsys.readouterr()
    assert "Buzzard Power Suite Version" in captured.out


def test_cli_status(capsys):
    dispatch(["status"])
    captured = capsys.readouterr()
    assert "System Power Status" in captured.out


def test_cli_doctor(capsys):
    dispatch(["doctor"])
    captured = capsys.readouterr()
    assert "System Doctor Diagnostics" in captured.out


def test_cli_invalid_command(capsys):
    dispatch(["invalid_command_xyz"])
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out
