"""Buzzard CLI Command: Meeting Profile.

Applies the declarative quiet meeting profile via ProfileService.
"""

from buzzard.colors import Console
from buzzard.services.profile_service import ProfileService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Applies meeting profile.

    Args:
        args: Command line arguments.
    """
    banner("Applying Profile: Meeting Mode")

    success, results = ProfileService.apply_profile("meeting")

    for res in results:
        if res.success:
            Console.success(f"  [OK] {res.message}")
        else:
            Console.error(f"  [FAIL] {res.message}")

    if success:
        Console.success("\nMeeting mode profile applied successfully.")
    else:
        Console.error("\nFailed to apply meeting profile fully. Rollback executed.")
