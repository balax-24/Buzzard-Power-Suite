"""Buzzard CLI Command: Daemon.

Runs power management daemon loop or installs Systemd user service.
"""

from buzzard.colors import Console
from buzzard.services.daemon_service import DaemonService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Executes daemon command.

    Args:
        args: Command line arguments.
    """
    banner("Power Management Daemon")

    if args and "--install" in args:
        res = DaemonService.install_systemd_service()
        if res.success:
            Console.success(res.message)
        else:
            Console.error(res.message)
        return

    Console.info("Starting background power daemon loop (Press Ctrl+C to exit)...")
    DaemonService.run_daemon_loop()
