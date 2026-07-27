"""Buzzard CLI Command: Restore.

Restores the system to the previously recorded active profile state via RestoreService.
"""

from buzzard.colors import Console
from buzzard.services.restore_service import RestoreService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Executes profile restoration command.

    Args:
        args: Command line arguments.
    """
    banner("Restoring Previous Profile")

    success, results = RestoreService.restore_previous()

    for res in results:
        if res.success:
            Console.success(f"  [OK] {res.message}")
        else:
            Console.error(f"  [FAIL] {res.message}")

    if success:
        Console.success("\nPrevious profile restored successfully.")
    else:
        Console.error("\nFailed to restore previous profile state.")
