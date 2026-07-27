"""Buzzard CLI Command: Travel Profile.

Applies the declarative travel power saver profile via ProfileService.
"""

from buzzard.colors import Console
from buzzard.services.profile_service import ProfileService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Applies travel profile.

    Args:
        args: Command line arguments.
    """
    banner("Applying Profile: Travel Mode")

    success, results = ProfileService.apply_profile("travel")

    for res in results:
        if res.success:
            Console.success(f"  [OK] {res.message}")
        else:
            Console.error(f"  [FAIL] {res.message}")

    if success:
        Console.success("\nTravel profile applied successfully.")
    else:
        Console.error("\nFailed to apply travel profile fully. Rollback executed.")
