"""Buzzard CLI Command: MacMode Profile.

Applies Apple Silicon MacBook-equivalent battery tuning targeting ~3.5W - 5.0W discharge rates.
"""

from buzzard.colors import Console
from buzzard.services.profile_service import ProfileService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Applies MacMode ultra power saver profile.

    Args:
        args: Command line arguments.
    """
    banner("Applying Profile: MacMode Ultra Power Saver")

    success, results = ProfileService.apply_profile("macmode")

    for res in results:
        if res.success:
            Console.success(f"  [OK] {res.message}")
        else:
            Console.error(f"  [FAIL] {res.message}")

    if success:
        Console.success("\nMacMode profile applied successfully! Battery power draw targeted at ~3.5W-5.0W.")
    else:
        Console.error("\nFailed to apply MacMode profile fully. Rollback executed.")
