"""Buzzard CLI Command: Full Power Profile.

Applies the declarative full performance profile via ProfileService.
"""

from buzzard.colors import Console
from buzzard.services.profile_service import ProfileService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Applies full performance profile.

    Args:
        args: Command line arguments.
    """
    banner("Applying Profile: Full Power")

    success, results = ProfileService.apply_profile("full")

    for res in results:
        if res.success:
            Console.success(f"  [OK] {res.message}")
        else:
            Console.error(f"  [FAIL] {res.message}")

    if success:
        Console.success("\nFull performance profile applied successfully.")
    else:
        Console.error("\nFailed to apply full power profile fully. Rollback executed.")
