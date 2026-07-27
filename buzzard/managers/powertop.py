"""PowerTOP Optimization Manager.

Manages PowerTOP autotuning system optimizations.
IMPORTANT: PowerTOP MUST NEVER BE EXECUTED AUTOMATICALLY.
It is strictly invoked via explicit 'buzzard optimize' user requests.
"""

from buzzard.core.result import Result
from buzzard.core.shell import Shell


class PowerTOPManager:
    """PowerTOP Optimization Subsystem Manager."""

    @staticmethod
    def is_installed() -> bool:
        """Checks if powertop is installed on the host system.

        Returns:
            True if powertop binary exists in PATH.
        """
        return Shell.exists("powertop")

    @staticmethod
    def autotune() -> Result:
        """Runs PowerTOP auto-tune system power optimizations.

        Returns:
            Result object.
        """
        if not PowerTOPManager.is_installed():
            return Result(
                success=False,
                message="PowerTOP is not installed on this system",
            )

        res = Shell.run("sudo powertop --auto-tune", use_shell=True)
        if res.success:
            return Result(
                success=True,
                message="PowerTOP autotune optimizations applied successfully",
                stdout=res.stdout,
                rollback_available=False,
            )
        return Result(
            success=False,
            message=f"PowerTOP autotune failed: {res.stderr}",
            stderr=res.stderr,
        )
