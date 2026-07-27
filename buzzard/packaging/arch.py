"""Arch Linux PKGBUILD Generator for Buzzard Power Suite."""

from pathlib import Path
from buzzard import __version__


class ArchPackager:
    """Generates Arch Linux PKGBUILD manifest."""

    @classmethod
    def generate_pkgbuild(cls, output_dir: Path) -> Path:
        """Creates PKGBUILD file for Arch User Repository (AUR).

        Args:
            output_dir: Target output directory.

        Returns:
            Path to generated PKGBUILD file.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        pkgbuild_content = f"""# Maintainer: Buzzard Power Suite Developers <dev@buzzard.org>
pkgname=buzzard-power-suite
pkgver={__version__}
pkgrel=1
pkgdesc="Universal Linux Power Management & AI Adaptive Workload Suite"
arch=('any')
url="https://github.com/buzzard/buzzard-power-suite"
license=('MIT')
depends=('python>=3.12' 'python-gobject' 'tlp' 'powertop' 'acpi' 'power-profiles-daemon')
makedepends=('python-setuptools' 'python-build' 'python-installer' 'python-wheel')
source=("$pkgname-$pkgver.tar.gz")
sha256sums=('SKIP')

build() {{
    cd "$pkgname-$pkgver"
    python -m build --wheel --no-isolation
}}

package() {{
    cd "$pkgname-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
}}
"""
        pkgbuild_path = output_dir / "PKGBUILD"
        pkgbuild_path.write_text(pkgbuild_content, encoding="utf-8")
        return pkgbuild_path
