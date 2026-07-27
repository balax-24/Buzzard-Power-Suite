"""Buzzard Profile Restoration Service.

Restores the system state to the previously saved active profile configuration.
"""

from typing import List, Tuple
from buzzard.core.result import Result
from buzzard.services.profile_service import ProfileService


class RestoreService:
    """Service for restoring previous power profile states."""

    @classmethod
    def restore_previous(cls) -> Tuple[bool, List[Result]]:
        """Restores system to previous saved profile state.

        Returns:
            Tuple of (success boolean, list of Result objects).
        """
        prev = ProfileService.previous()
        if prev == "None" or prev == "Unknown":
            return False, [
                Result(
                    success=False,
                    message="No previous profile recorded to restore",
                )
            ]

        curr = ProfileService.current()
        if prev == curr:
            return True, [
                Result(
                    success=True,
                    message=f"System is already running previous profile '{prev}'",
                )
            ]

        return ProfileService.apply_profile(prev)
