"""Linux Distribution and Package Manager Introspection Module.

Identifies Linux distro release (/etc/os-release), detects active package manager
(apt, pacman, dnf, zypper), and maps required power management dependencies.
"""

import os
from pathlib import Path
from typing import Dict, List
from buzzard.core.shell import Shell


class DistroDetector:
    """Linux Distribution and Package Manager Introspector."""

    OS_RELEASE = Path("/etc/os-release")

    @classmethod
    def get_info(cls) -> Dict[str, str]:
        """Parses /etc/os-release to identify Linux distribution details.

        Returns:
            Dictionary with keys 'id', 'name', 'version', 'id_like'.
        """
        info = {"id": "generic", "name": "Generic Linux", "version": "", "id_like": ""}
        if cls.OS_RELEASE.exists():
            try:
                for line in cls.OS_RELEASE.read_text(encoding="utf-8").splitlines():
                    if "=" in line:
                        k, v = line.split("=", 1)
                        v = v.strip('"\'')
                        if k == "ID":
                            info["id"] = v.lower()
                        elif k == "NAME":
                            info["name"] = v
                        elif k == "VERSION_ID":
                            info["version"] = v
                        elif k == "ID_LIKE":
                            info["id_like"] = v.lower()
            except Exception:
                pass

        return info

    @classmethod
    def get_package_manager(cls) -> str:
        """Detects system package manager.

        Returns:
            Package manager identifier string ('apt', 'pacman', 'dnf', 'zypper', 'unknown').
        """
        if Shell.exists("apt-get") or Shell.exists("apt"):
            return "apt"
        if Shell.exists("pacman"):
            return "pacman"
        if Shell.exists("dnf"):
            return "dnf"
        if Shell.exists("zypper"):
            return "zypper"
        return "unknown"

    @classmethod
    def get_dependency_packages(cls) -> List[str]:
        """Returns distro-specific package names for required power suite tools & modules.

        (TLP, PowerTOP, power-profiles-daemon/powerctl, xrandr, libnotify, gobject, cpupower).

        Returns:
            List of package names for the active package manager.
        """
        pm = cls.get_package_manager()
        distro_id = cls.get_info()["id"]

        if pm == "apt":
            pkgs = [
                "tlp",
                "powertop",
                "x11-xserver-utils",
                "libnotify-bin",
                "python3-gi",
                "gir1.2-appindicator3-0.1",
                "power-profiles-daemon",
                "linux-tools-common",
                "acpi",
            ]
            return pkgs

        if pm == "pacman":
            pkgs = [
                "tlp",
                "powertop",
                "xorg-xrandr",
                "libnotify",
                "python-gobject",
                "libappindicator-gtk3",
                "power-profiles-daemon",
                "acpi",
            ]
            return pkgs

        if pm == "dnf":
            pkgs = [
                "tlp",
                "powertop",
                "xrandr",
                "libnotify",
                "python3-gobject",
                "libappindicator-gtk3",
                "power-profiles-daemon",
                "kernel-tools",
                "acpi",
            ]
            return pkgs

        if pm == "zypper":
            pkgs = [
                "tlp",
                "powertop",
                "xrandr",
                "libnotify-tools",
                "python3-gobject",
                "power-profiles-daemon",
                "acpi",
            ]
            return pkgs

        return ["tlp", "powertop", "xrandr", "power-profiles-daemon"]

    @classmethod
    def get_install_command(cls) -> str:
        """Returns command string to install missing system packages.

        Returns:
            Command string with sudo prefix.
        """
        pm = cls.get_package_manager()
        pkgs = " ".join(cls.get_dependency_packages())

        if pm == "apt":
            return f"sudo apt-get update && sudo apt-get install -y {pkgs}"
        if pm == "pacman":
            return f"sudo pacman -Sy --needed --noconfirm {pkgs}"
        if pm == "dnf":
            return f"sudo dnf install -y {pkgs}"
        if pm == "zypper":
            return f"sudo zypper install -y {pkgs}"

        return f"echo 'Please manually install: {pkgs}'"
