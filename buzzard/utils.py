"""Utility helper methods for Buzzard Power Suite.

Routes all system requests through the central Shell engine.
"""

from typing import Union
from buzzard.core.shell import Shell, ShellResult


def run(command: Union[str, list[str]], use_shell: bool = True) -> ShellResult:
    """Helper wrapper for running shell commands.

    Args:
        command: Command string or list.
        use_shell: Whether to use shell interpreter.

    Returns:
        ShellResult object.
    """
    return Shell.run(command, use_shell=use_shell)


def exists(binary: str) -> bool:
    """Helper wrapper to check if a binary exists in system PATH.

    Args:
        binary: Binary executable name.

    Returns:
        True if executable exists.
    """
    return Shell.exists(binary)