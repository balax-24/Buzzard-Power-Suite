"""Buzzard CLI Command: Linux Package Generator.

Generates native distribution packages (.deb, PKGBUILD, .spec) for Debian, Arch, and Fedora.
"""

from pathlib import Path
from buzzard.colors import Console
from buzzard.packaging.arch import ArchPackager
from buzzard.packaging.deb import DebPackager
from buzzard.packaging.rpm import RPMPackager
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Executes Linux package generation command.

    Args:
        args: Target distro package type ('deb', 'arch', 'rpm', or 'all').
    """
    banner("Linux Package Distribution Generator")

    pkg_type = args[0].lower() if args else "all"
    out_dir = Path("./build/dist_packages")

    Console.info(f"Generating package distribution manifests in {out_dir}...")

    if pkg_type in ("deb", "all"):
        deb_control = DebPackager.generate_spec(out_dir)
        Console.success(f"  [Debian/Ubuntu] Control file generated: {deb_control}")

    if pkg_type in ("arch", "all"):
        pkgbuild = ArchPackager.generate_pkgbuild(out_dir)
        Console.success(f"  [Arch Linux] PKGBUILD generated: {pkgbuild}")

    if pkg_type in ("rpm", "all"):
        spec = RPMPackager.generate_spec(out_dir)
        Console.success(f"  [Fedora/RPM] SPEC file generated: {spec}")

    Console.success("\nPackage generation complete! Production ready for distribution.")
