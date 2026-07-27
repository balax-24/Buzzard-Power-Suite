"""Buzzard Configuration and Profile Loader.

Loads declarative YAML profiles with hierarchical inheritance:
Base (generic/profile.yaml) -> Vendor Override (vendor_id/profile.yaml) -> User Custom Override (~/.config/buzzard/profiles/profile.yaml).
"""

from pathlib import Path
from typing import Any, Dict, List
import yaml
from buzzard.core.constants import BASE_DIR, USER_CONFIG_DIR
from buzzard.plugins.manager import PluginManager


class ConfigManager:
    """Manager for loading declarative YAML power profiles."""

    PROFILES_DIR = BASE_DIR / "profiles"

    @classmethod
    def list_available_profiles(cls) -> List[str]:
        """Lists all available profile names.

        Returns:
            List of profile names (e.g. ['low', 'hybrid', 'full', 'gaming']).
        """
        profiles = set()

        # Generic profiles directory
        generic_dir = cls.PROFILES_DIR / "generic"
        if generic_dir.exists():
            for p in generic_dir.glob("*.yaml"):
                profiles.add(p.stem)

        # User custom profiles directory
        user_profiles_dir = USER_CONFIG_DIR / "profiles"
        if user_profiles_dir.exists():
            for p in user_profiles_dir.glob("*.yaml"):
                profiles.add(p.stem)

        return sorted(list(profiles))

    @classmethod
    def load_profile(cls, profile_name: str) -> Dict[str, Any]:
        """Loads and merges profile configuration hierarchically.

        Resolution order:
        1. Generic profile: profiles/generic/{profile_name}.yaml
        2. Vendor override: profiles/{vendor_id}/{profile_name}.yaml
        3. User override: ~/.config/buzzard/profiles/{profile_name}.yaml

        Args:
            profile_name: Profile name string.

        Returns:
            Merged profile payload dictionary.
        """
        merged_cfg: Dict[str, Any] = {}
        vendor_id = PluginManager.active_vendor_id()

        # 1. Base Generic Profile
        generic_file = cls.PROFILES_DIR / "generic" / f"{profile_name}.yaml"
        if generic_file.exists():
            content = generic_file.read_text(encoding="utf-8")
            cfg = yaml.safe_load(content)
            if isinstance(cfg, dict):
                merged_cfg.update(cfg)

        # 2. Vendor Override
        vendor_file = cls.PROFILES_DIR / vendor_id / f"{profile_name}.yaml"
        if vendor_file.exists():
            content = vendor_file.read_text(encoding="utf-8")
            vendor_cfg = yaml.safe_load(content)
            if isinstance(vendor_cfg, dict):
                cls._deep_merge(merged_cfg, vendor_cfg)

        # 3. User Custom Override
        user_file = USER_CONFIG_DIR / "profiles" / f"{profile_name}.yaml"
        if user_file.exists():
            content = user_file.read_text(encoding="utf-8")
            user_cfg = yaml.safe_load(content)
            if isinstance(user_cfg, dict):
                cls._deep_merge(merged_cfg, user_cfg)

        if not merged_cfg:
            raise FileNotFoundError(f"Profile '{profile_name}' not found in system or user configuration.")

        return merged_cfg

    @classmethod
    def _deep_merge(cls, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """Deeply merges dictionary keys into base dict in place.

        Args:
            base: Base target dictionary.
            override: Source dictionary containing override fields.
        """
        for key, val in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(val, dict):
                cls._deep_merge(base[key], val)
            else:
                base[key] = val
