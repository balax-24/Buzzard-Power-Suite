"""Profile Manager.

Loads declarative YAML profiles and exposes profile metadata to services.
"""

from typing import Any, Dict, List
from buzzard.core.config import ConfigManager


class ProfileManager:
    """Manager for loading declarative profiles."""

    @classmethod
    def load_profile(cls, profile_name: str) -> Dict[str, Any]:
        """Loads and parses a profile configuration.

        Args:
            profile_name: Name of profile (low, hybrid, gaming, etc.).

        Returns:
            Validated profile dictionary.
        """
        return ConfigManager.load_profile(profile_name)

    @classmethod
    def list_profiles(cls) -> List[str]:
        """Lists available declarative profiles.

        Returns:
            List of profile names.
        """
        return ConfigManager.list_available_profiles()
