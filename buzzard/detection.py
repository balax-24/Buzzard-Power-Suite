"""
Hardware detection for Buzzard.
"""

from pathlib import Path
import platform


class Detection:

    @staticmethod
    def _read(path: str, default: str = "Unknown") -> str:
        try:
            return Path(path).read_text().strip()
        except Exception:
            return default

    @classmethod
    def vendor(cls) -> str:
        return cls._read("/sys/class/dmi/id/sys_vendor")

    @classmethod
    def product(cls) -> str:
        return cls._read("/sys/class/dmi/id/product_name")

    @classmethod
    def bios(cls) -> str:
        return cls._read("/sys/class/dmi/id/bios_version")

    @classmethod
    def kernel(cls) -> str:
        return platform.release()

    @classmethod
    def hostname(cls) -> str:
        return platform.node()

    @classmethod
    def architecture(cls) -> str:
        return platform.machine()
