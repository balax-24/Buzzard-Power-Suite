"""Fedora / RHEL RPM Spec Generator for Buzzard Power Suite."""

from pathlib import Path
from buzzard import __version__


class RPMPackager:
    """Generates Fedora / RHEL RPM spec file."""

    @classmethod
    def generate_spec(cls, output_dir: Path) -> Path:
        """Creates RPM spec file for Fedora COPR / packaging.

        Args:
            output_dir: Target output directory.

        Returns:
            Path to generated .spec file.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        spec_content = f"""Name:           buzzard-power-suite
Version:        {__version__}
Release:        1%{{?dist}}
Summary:        Universal Linux Power Management & AI Adaptive Workload Suite

License:        MIT
URL:            https://github.com/buzzard/buzzard-power-suite
Source0:        %{{name}}-%{{version}}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel python3-setuptools python3-pip
Requires:       python3 >= 3.12, python3-gobject, tlp, powertop, acpi, power-profiles-daemon

%description
Universal Linux Power Management & AI Adaptive Workload Suite providing advanced OEM power tuning,
MacMode ultra-low battery optimization (~3.5W-5W), and dynamic GUI system tray.

%prep
%autosetup

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
%doc README.md
%{{_bindir}}/buzzard
%{{_bindir}}/buzzard-gui
%{{python3_sitelib}}/buzzard/

%changelog
* Mon Jul 27 2026 Buzzard Developers <dev@buzzard.org> - {__version__}-1
- Release {__version__} 1.0.0 Production milestone.
"""
        spec_path = output_dir / "buzzard-power-suite.spec"
        spec_path.write_text(spec_content, encoding="utf-8")
        return spec_path
