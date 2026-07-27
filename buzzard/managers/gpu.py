"""GPU Hardware Subsystem Manager.

Handles hybrid graphics switching (prime-select, nvidia-smi, sysfs query)
and returns structured Result objects for all operations.
"""

from buzzard.core.result import Result
from buzzard.core.shell import Shell


class GPUManager:
    """GPU Hardware Control Manager."""

    @staticmethod
    def current() -> str:
        """Queries the active GPU graphics profile.

        Returns:
            String indicating active GPU mode (intel, nvidia, hybrid, or unknown).
        """
        if Shell.exists("prime-select"):
            r = Shell.run("prime-select query")
            if r.success and r.stdout:
                return r.stdout.strip().lower()

        # Fallback check via nvidia-smi
        if Shell.exists("nvidia-smi"):
            nsmi = Shell.run("nvidia-smi")
            if nsmi.success:
                return "nvidia"

        return "intel"

    @staticmethod
    def use_intel() -> Result:
        """Switches GPU mode to Integrated Intel graphics.

        Returns:
            Result object indicating success and reboot requirement.
        """
        curr = GPUManager.current()
        if curr == "intel":
            return Result(success=True, message="GPU is already set to Intel")

        if Shell.exists("prime-select"):
            res = Shell.run("sudo prime-select intel")
            if res.success:
                return Result(
                    success=True,
                    message="Switched GPU mode to Intel (Reboot Required)",
                    stdout=res.stdout,
                    reboot_required=True,
                    rollback_available=True,
                )
            return Result(
                success=False,
                message=f"Failed to switch GPU to Intel: {res.stderr}",
                stderr=res.stderr,
            )

        return Result(
            success=False,
            message="prime-select command not available on this system",
        )

    @staticmethod
    def use_nvidia() -> Result:
        """Switches GPU mode to Dedicated NVIDIA graphics.

        Returns:
            Result object indicating success and reboot requirement.
        """
        curr = GPUManager.current()
        if curr == "nvidia":
            return Result(success=True, message="GPU is already set to NVIDIA")

        if Shell.exists("prime-select"):
            res = Shell.run("sudo prime-select nvidia")
            if res.success:
                return Result(
                    success=True,
                    message="Switched GPU mode to NVIDIA (Reboot Required)",
                    stdout=res.stdout,
                    reboot_required=True,
                    rollback_available=True,
                )
            return Result(
                success=False,
                message=f"Failed to switch GPU to NVIDIA: {res.stderr}",
                stderr=res.stderr,
            )

        return Result(
            success=False,
            message="prime-select command not available on this system",
        )

    @staticmethod
    def use_hybrid() -> Result:
        """Switches GPU mode to Hybrid / On-Demand graphics mode.

        Returns:
            Result object.
        """
        curr = GPUManager.current()
        if curr in ("on-demand", "hybrid"):
            return Result(success=True, message="GPU is already set to Hybrid")

        if Shell.exists("prime-select"):
            res = Shell.run("sudo prime-select on-demand")
            if res.success:
                return Result(
                    success=True,
                    message="Switched GPU mode to Hybrid (Reboot Required)",
                    stdout=res.stdout,
                    reboot_required=True,
                    rollback_available=True,
                )
            return Result(
                success=False,
                message=f"Failed to switch GPU to Hybrid: {res.stderr}",
                stderr=res.stderr,
            )

        return Result(
            success=False,
            message="prime-select command not available on this system",
        )
