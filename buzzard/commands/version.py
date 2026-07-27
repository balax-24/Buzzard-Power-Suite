"""Buzzard CLI Command: Version.

Displays version details for Buzzard Power Suite.
"""

from buzzard import __version__
from buzzard.colors import Console
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Executes version command.

    Args:
        args: Command line arguments.
    """
    banner("Version Information")
    Console.info(f"Buzzard Power Suite Version: v{__version__}")
    Console.info("License: MIT")
    Console.info("Target Architecture: Linux (x86_64 / aarch64)")
