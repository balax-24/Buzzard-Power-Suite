"""Tests for declarative profile YAML loading and schema validation."""

import pytest
from buzzard.core.config import ConfigManager


def test_list_profiles():
    profiles = ConfigManager.list_available_profiles()
    assert "low" in profiles
    assert "hybrid" in profiles
    assert "full" in profiles
    assert "gaming" in profiles


@pytest.mark.parametrize("profile_name", ["low", "hybrid", "full", "gaming", "pentest", "llm", "dock"])
def test_load_all_profiles(profile_name):
    cfg = ConfigManager.load_profile(profile_name)
    assert "gpu" in cfg
    assert "cpu" in cfg
    assert "brightness" in cfg
    assert "bluetooth" in cfg
    assert "tlp" in cfg
    assert "powertop" in cfg
    assert isinstance(cfg["brightness"], int)
    assert 0 <= cfg["brightness"] <= 100
