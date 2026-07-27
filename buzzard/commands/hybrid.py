"""Buzzard CLI Command: Hybrid Profile.

Applies the declarative hybrid power profile via ProfileService.
"""

from buzzard.colors import Console
from buzzard.services.profile_service import ProfileService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Applies hybrid profile.

    Args:
        args: Command line arguments.
    """
    banner("Applying Profile: Hybrid Power")

    success, results = ProfileService.apply_profile("hybrid")

    for res in results:
        if res.success:
            Console.success(f"  [OK] {res.message}")
        else:
            Console.error(f"  [FAIL] {res.message}")

    if success:
        Console.success("\nHybrid profile applied successfully.")
    else:
        Console.error("\nFailed to apply hybrid profile fully. Rollback executed.")
