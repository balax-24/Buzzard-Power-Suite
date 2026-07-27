"""Buzzard Privilege Escalation and Polkit Configurator.

Generates and installs Sudoers and Polkit authorization rules allowing
passwordless sysfs writes and hardware power subsystem management.
"""

from pathlib import Path
from buzzard.core.result import Result
from buzzard.core.shell import Shell


class PrivilegeManager:
    """Manager for configuring Linux system privileges and Polkit/Sudoers rules."""

    SUDOERS_FILE = Path("/etc/sudoers.d/buzzard")
    POLKIT_FILE = Path("/etc/polkit-1/rules.d/99-buzzard.rules")

    @classmethod
    def is_configured(cls) -> bool:
        """Checks if Buzzard sudoers configuration file exists.

        Returns:
            Boolean true if configured.
        """
        return cls.SUDOERS_FILE.exists()

    @classmethod
    def setup_sudoers(cls) -> Result:
        """Generates and installs passwordless sudoers permissions file.

        Returns:
            Result object.
        """
        try:
            content = """# Buzzard Power Suite Sudoers Rules
ALL ALL=(ALL) NOPASSWD: /usr/bin/tee, /usr/bin/tlp, /usr/bin/powertop, /usr/bin/powerprofilesctl
"""
            # Write via sudo tee to /etc/sudoers.d/buzzard
            cmd = f"echo '{content}' | sudo tee {cls.SUDOERS_FILE}"
            res = Shell.run(cmd, use_shell=True)

            if res.success:
                Shell.run(f"sudo chmod 0440 {cls.SUDOERS_FILE}", use_shell=True)
                return Result(
                    success=True,
                    message=f"Sudoers rule created at {cls.SUDOERS_FILE}",
                )
            return Result(
                success=False,
                message=f"Failed writing sudoers file: {res.stderr}",
            )
        except Exception as exc:
            return Result(
                success=False,
                message=f"Privilege setup error: {exc}",
            )
