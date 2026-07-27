"""Buzzard Power Management Daemon Service.

Monitors AC power plug/unplug events and battery state changes, auto-switching profiles,
and manages Systemd user service installation.
"""

from pathlib import Path
import time
from buzzard.core.logger import Logger
from buzzard.core.result import Result
from buzzard.core.shell import Shell
from buzzard.managers import BatteryManager
from buzzard.services.profile_service import ProfileService

logger = Logger()


class DaemonService:
    """Service for running power daemon loop and systemd integration."""

    SYSTEMD_USER_DIR = Path.home() / ".config" / "systemd" / "user"
    SERVICE_FILE = SYSTEMD_USER_DIR / "buzzard-daemon.service"

    @classmethod
    def run_daemon_loop(cls, poll_interval: int = 5) -> None:
        """Runs foreground daemon loop monitoring AC power state changes.

        Args:
            poll_interval: Seconds between state checks.
        """
        logger.info("Buzzard Power Daemon started.")
        last_ac = BatteryManager.is_ac_connected()

        while True:
            try:
                current_ac = BatteryManager.is_ac_connected()
                if current_ac != last_ac:
                    logger.info(f"Power source change detected (AC Connected: {current_ac}). Auto-applying profile.")
                    ProfileService.apply_auto()
                    last_ac = current_ac
                time.sleep(poll_interval)
            except KeyboardInterrupt:
                logger.info("Buzzard Power Daemon stopping.")
                break
            except Exception as exc:
                logger.error(f"Error in daemon loop: {exc}")
                time.sleep(poll_interval)

    @classmethod
    def install_systemd_service(cls) -> Result:
        """Installs and enables Systemd user daemon service.

        Returns:
            Result object.
        """
        try:
            cls.SYSTEMD_USER_DIR.mkdir(parents=True, exist_ok=True)
            python_bin = Shell.run("which python3").stdout.strip() or "/usr/bin/python3"

            service_content = f"""[Unit]
Description=Buzzard Power Suite Background Daemon
After=multi-user.target

[Service]
Type=simple
ExecStart={python_bin} -m buzzard.cli daemon
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=default.target
"""
            cls.SERVICE_FILE.write_text(service_content, encoding="utf-8")

            # Reload systemd and enable service
            Shell.run("systemctl --user daemon-reload")
            res = Shell.run("systemctl --user enable --now buzzard-daemon.service")

            if res.success:
                return Result(
                    success=True,
                    message="Buzzard Systemd User Daemon installed and activated successfully.",
                )

            return Result(
                success=True,
                message=f"Buzzard Systemd User Daemon service file written to {cls.SERVICE_FILE}",
            )
        except Exception as exc:
            return Result(
                success=False,
                message=f"Failed installing systemd service: {exc}",
            )
