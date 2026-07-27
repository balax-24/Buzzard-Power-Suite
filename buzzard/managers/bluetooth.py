"""Bluetooth Wireless Subsystem Manager.

Controls Bluetooth radio states using rfkill utility and returns structured Result objects.
"""

from buzzard.core.result import Result
from buzzard.core.shell import Shell


class BluetoothManager:
    """Bluetooth Subsystem Power State Manager."""

    @staticmethod
    def status() -> str:
        """Queries the current Bluetooth soft-block status.

        Returns:
            String ('Enabled', 'Disabled', or 'Unknown').
        """
        if Shell.exists("rfkill"):
            r = Shell.run("rfkill list bluetooth")
            if r.success and r.stdout:
                if "Soft blocked: yes" in r.stdout:
                    return "Disabled"
                if "Soft blocked: no" in r.stdout:
                    return "Enabled"

        return "Unknown"

    @staticmethod
    def is_enabled() -> bool:
        """Checks if Bluetooth radio is currently unblocked/enabled.

        Returns:
            True if enabled, False otherwise.
        """
        return BluetoothManager.status() == "Enabled"

    @staticmethod
    def disable() -> Result:
        """Disables the Bluetooth radio via rfkill soft-block.

        Returns:
            Result object.
        """
        if BluetoothManager.status() == "Disabled":
            return Result(success=True, message="Bluetooth radio is already disabled")

        if Shell.exists("rfkill"):
            r = Shell.run("sudo rfkill block bluetooth", use_shell=True)
            if r.success:
                return Result(
                    success=True,
                    message="Bluetooth radio disabled",
                    stdout=r.stdout,
                    rollback_available=True,
                )
            return Result(
                success=False,
                message=f"Failed to block bluetooth radio: {r.stderr}",
                stderr=r.stderr,
            )

        return Result(success=False, message="rfkill command not found")

    @staticmethod
    def enable() -> Result:
        """Enables the Bluetooth radio via rfkill unblock.

        Returns:
            Result object.
        """
        if BluetoothManager.status() == "Enabled":
            return Result(success=True, message="Bluetooth radio is already enabled")

        if Shell.exists("rfkill"):
            r = Shell.run("sudo rfkill unblock bluetooth", use_shell=True)
            if r.success:
                return Result(
                    success=True,
                    message="Bluetooth radio enabled",
                    stdout=r.stdout,
                    rollback_available=True,
                )
            return Result(
                success=False,
                message=f"Failed to unblock bluetooth radio: {r.stderr}",
                stderr=r.stderr,
            )

        return Result(success=False, message="rfkill command not found")
