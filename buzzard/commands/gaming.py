"""Buzzard CLI Command: Gaming Profile.

Applies the declarative gaming performance profile via ProfileService.
"""

from buzzard.colors import Console
from buzzard.services.profile_service import ProfileService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Applies gaming profile.

    Args:
        args: Command line arguments.
    """
    banner("Applying Profile: Gaming Mode")

    success, results = ProfileService.apply_profile("gaming")

    for res in results:
        if res.success:
            Console.success(f"  [OK] {res.message}")
        else:
            Console.error(f"  [FAIL] {res.message}")

    if success:
        Console.success("\nGaming profile applied successfully.")
    else:
        Console.error("\nFailed to apply gaming profile fully. Rollback executed.")
