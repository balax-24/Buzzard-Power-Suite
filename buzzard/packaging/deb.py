"""Debian / Ubuntu Package Generator for Buzzard Power Suite."""

import os
from pathlib import Path
from buzzard import __version__
from buzzard.core.shell import Shell


class DebPackager:
    """Generates Debian / Ubuntu .deb package structures."""

    @classmethod
    def generate_spec(cls, output_dir: Path) -> Path:
        """Creates Debian package directory structure and control file.

        Args:
            output_dir: Target output directory.

        Returns:
            Path to generated DEBIAN/control file.
        """
        deb_dir = output_dir / f"buzzard-power-suite_{__version__}_amd64"
        debian_meta = deb_dir / "DEBIAN"
        debian_meta.mkdir(parents=True, exist_ok=True)

        control_content = f"""Package: buzzard-power-suite
Version: {__version__}
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Buzzard Power Suite Developers <dev@buzzard.org>
Depends: python3 (>= 3.12), python3-gobject, tlp, powertop, acpi, power-profiles-daemon
Description: Universal Linux Power Management & AI Adaptive Workload Suite
 Advanced OEM power tuning, MacMode ultra-low battery optimization, and dynamic GUI system tray.
"""
        control_path = debian_meta / "control"
        control_path.write_text(control_content, encoding="utf-8")
        return control_path
