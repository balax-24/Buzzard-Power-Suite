"""Global constants for Buzzard Power Suite.

Centralized paths, profile names, versioning, and default configurations.
"""

from pathlib import Path
from buzzard import __version__

APP_NAME = "Buzzard Power Suite"
VERSION = __version__

# Filesystem Paths
HOME = Path.home()
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = HOME / ".config" / "buzzard"
USER_CONFIG_DIR = CONFIG_DIR
DATA_DIR = HOME / ".local" / "share" / "buzzard"
LOG_DIR = DATA_DIR / "logs"
LOG_FILE = LOG_DIR / "buzzard.log"
HISTORY_FILE = DATA_DIR / "history.json"

CURRENT_PROFILE_FILE = CONFIG_DIR / "current_profile"
PREVIOUS_PROFILE_FILE = CONFIG_DIR / "previous_profile"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

# Supported Profiles
VALID_PROFILES = [
    "low",
    "hybrid",
    "gaming",
    "full",
    "creator",
    "travel",
    "meeting",
    "pentest",
    "llm",
    "dock",
]

# Standard System Defaults
DEFAULT_PROFILE = "hybrid"

# Vendor Identifiers
VENDOR_ASUS = "ASUSTeK COMPUTER INC."
VENDOR_LENOVO = "LENOVO"
VENDOR_DELL = "Dell Inc."
VENDOR_HP = "HP"
VENDOR_GENERIC = "Generic"
