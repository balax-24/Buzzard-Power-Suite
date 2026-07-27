"""Buzzard CLI Command: Creator Profile.

Applies the declarative creator profile via ProfileService.
"""

from buzzard.colors import Console
from buzzard.services.profile_service import ProfileService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Applies creator profile.

    Args:
        args: Command line arguments.
    """
    banner("Applying Profile: Creator Mode")

    success, results = ProfileService.apply_profile("creator")

    for res in results:
        if res.success:
            Console.success(f"  [OK] {res.message}")
        else:
            Console.error(f"  [FAIL] {res.message}")

    if success:
        Console.success("\nCreator mode profile applied successfully.")
    else:
        Console.error("\nFailed to apply creator profile fully. Rollback executed.")
