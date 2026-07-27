"""Buzzard CLI Command: Low Power Profile.

Applies the declarative low power profile via ProfileService.
"""

from buzzard.colors import Console
from buzzard.services.profile_service import ProfileService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Applies low power profile.

    Args:
        args: Command line arguments.
    """
    banner("Applying Profile: Low Power")

    success, results = ProfileService.apply_profile("low")

    for res in results:
        if res.success:
            Console.success(f"  [OK] {res.message}")
        else:
            Console.error(f"  [FAIL] {res.message}")

    if success:
        Console.success("\nLow power profile applied successfully.")
    else:
        Console.error("\nFailed to apply low power profile fully. Rollback executed.")
