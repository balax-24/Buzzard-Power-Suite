"""TLP Power Management Daemon Manager.

Interacts with TLP daemon and tlp-stat utility to start, stop, or query
system TLP power profiles.
"""

from buzzard.core.result import Result
from buzzard.core.shell import Shell


class TLPManager:
    """TLP Linux Power Optimizer Daemon Manager."""

    @staticmethod
    def is_installed() -> bool:
        """Checks if TLP is installed on the host system.

        Returns:
            True if tlp executable exists.
        """
        return Shell.exists("tlp")

    @staticmethod
    def status() -> str:
        """Queries current TLP operational status.

        Returns:
            String ('Active', 'Inactive', or 'Not Installed').
        """
        if not TLPManager.is_installed():
            return "Not Installed"

        r = Shell.run("tlp-stat -s")
        if r.success and "State = enabled" in r.stdout:
            return "Active"
        return "Inactive"

    @staticmethod
    def start() -> Result:
        """Starts / refreshes TLP power optimizations.

        Returns:
            Result object.
        """
        if not TLPManager.is_installed():
            return Result(success=False, message="TLP is not installed")

        res = Shell.run("sudo tlp start", use_shell=True)
        if res.success:
            return Result(
                success=True,
                message="TLP power management daemon started",
                stdout=res.stdout,
            )
        return Result(
            success=False,
            message=f"Failed starting TLP daemon: {res.stderr}",
            stderr=res.stderr,
        )

    @staticmethod
    def stop() -> Result:
        """Stops TLP power optimizations.

        Returns:
            Result object.
        """
        if not TLPManager.is_installed():
            return Result(success=False, message="TLP is not installed")

        res = Shell.run("sudo tlp turnoff", use_shell=True)
        if res.success:
            return Result(
                success=True,
                message="TLP power management daemon disabled",
                stdout=res.stdout,
            )
        return Result(
            success=False,
            message=f"Failed stopping TLP daemon: {res.stderr}",
            stderr=res.stderr,
        )
