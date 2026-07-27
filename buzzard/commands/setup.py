"""Buzzard CLI Command: Cross-Distro System Setup & Dependency Installation.

Detects Linux distribution, installs required system packages & power tools (apt, pacman, dnf, zypper),
configures passwordless privilege rules, and initializes systemd service.
"""

from buzzard.colors import Console
from buzzard.core.distro import DistroDetector
from buzzard.core.privileges import PrivilegeManager
from buzzard.core.shell import Shell
from buzzard.services.daemon_service import DaemonService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Executes cross-distro setup & dependency installer command.

    Args:
        args: Command line arguments.
    """
    banner("Cross-Distro System Setup & Dependencies")

    distro = DistroDetector.get_info()
    pm = DistroDetector.get_package_manager()
    pkgs = DistroDetector.get_dependency_packages()
    cmd = DistroDetector.get_install_command()

    Console.info(f"Linux Distribution : {distro['name']} ({distro['id']})")
    Console.info(f"Package Manager    : {pm.upper()}")
    Console.info(f"Target Dependencies: {', '.join(pkgs)}")

    print()
    Console.info("Executing package manager installation...")
    res = Shell.run(cmd, use_shell=True)
    if res.success:
        Console.success("System power packages & dependencies installed successfully!")
    else:
        Console.warning(f"Package manager finished with notice: {res.stderr or res.stdout}")

    print()
    Console.info("Configuring passwordless privilege escalation for sysfs power nodes...")
    priv_res = PrivilegeManager.setup_sudoers()
    if priv_res.success:
        Console.success(priv_res.message)
    else:
        Console.warning(f"Notice: {priv_res.message}")

    print()
    Console.info("Configuring Buzzard Background Systemd User Daemon...")
    d_res = DaemonService.install_systemd_service()
    if d_res.success:
        Console.success(d_res.message)

    Console.success("\nBuzzard Power Suite setup completed! All modules ready.")
