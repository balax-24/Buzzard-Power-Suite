"""Unit tests for Release 10 features (Package Generator Engine & Version 1.0.0 Milestone)."""

from buzzard import __version__
from buzzard.packaging.arch import ArchPackager
from buzzard.packaging.deb import DebPackager
from buzzard.packaging.rpm import RPMPackager


def test_v1_0_0_milestone():
    assert __version__ == "1.0.0"


def test_deb_packager_generator(tmp_path):
    ctrl_file = DebPackager.generate_spec(tmp_path)
    assert ctrl_file.exists()
    content = ctrl_file.read_text(encoding="utf-8")
    assert "Package: buzzard-power-suite" in content
    assert "Version: 1.0.0" in content


def test_arch_packager_generator(tmp_path):
    pkgbuild = ArchPackager.generate_pkgbuild(tmp_path)
    assert pkgbuild.exists()
    content = pkgbuild.read_text(encoding="utf-8")
    assert "pkgname=buzzard-power-suite" in content
    assert "pkgver=1.0.0" in content


def test_rpm_packager_generator(tmp_path):
    spec_file = RPMPackager.generate_spec(tmp_path)
    assert spec_file.exists()
    content = spec_file.read_text(encoding="utf-8")
    assert "Name:           buzzard-power-suite" in content
    assert "Version:        1.0.0" in content
