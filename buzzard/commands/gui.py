"""Buzzard CLI Command: Desktop System Tray GUI Application Launcher."""

from buzzard.gui.app import main as launch_gui


def run(args: list[str] | None = None) -> None:
    """Launches Buzzard System Tray GUI Application."""
    launch_gui()
