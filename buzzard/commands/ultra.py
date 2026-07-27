"""Buzzard CLI Command: Ultra Saver Profile Alias.

Alias for MacMode ultra power saver profile.
"""

from buzzard.commands.macmode import run as macmode_run


def run(args: list[str] | None = None) -> None:
    """Executes ultra power saver command.

    Args:
        args: Command line arguments.
    """
    macmode_run(args)
