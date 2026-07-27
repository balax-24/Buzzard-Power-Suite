"""Buzzard CLI Command: Dock Profile.

Applies the declarative docked station profile via ProfileService.
"""

from buzzard.colors import Console
from buzzard.services.profile_service import ProfileService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Applies dock profile.

    Args:
        args: Command line arguments.
    """
    banner("Applying Profile: Docked Station")

    success, results = ProfileService.apply_profile("dock")

    for res in results:
        if res.success:
            Console.success(f"  [OK] {res.message}")
        else:
            Console.error(f"  [FAIL] {res.message}")

    if success:
        Console.success("\nDock profile applied successfully.")
    else:
        Console.error("\nFailed to apply dock profile fully. Rollback executed.")
