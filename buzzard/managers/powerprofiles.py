"""Power-Profiles-Daemon / Powerctl Manager.

Interacts with system power-profiles-daemon (powerprofilesctl / powerctl) to synchronize
Linux system power modes (performance, balanced, power-saver).
"""

from typing import List
from buzzard.core.result import Result
from buzzard.core.shell import Shell


class PowerProfilesManager:
    """Linux power-profiles-daemon Subsystem Manager."""

    @classmethod
    def exists(cls) -> bool:
        """Checks if powerprofilesctl or powerctl is available.

        Returns:
            Boolean true if available.
        """
        return Shell.exists("powerprofilesctl") or Shell.exists("powerctl")

    @classmethod
    def get_profile(cls) -> str:
        """Gets active powerprofile mode.

        Returns:
            Profile string ('performance', 'balanced', 'power-saver', 'unknown').
        """
        if Shell.exists("powerprofilesctl"):
            res = Shell.run("powerprofilesctl get")
            if res.success:
                return res.stdout.strip()

        if Shell.exists("powerctl"):
            res = Shell.run("powerctl get")
            if res.success:
                return res.stdout.strip()

        return "unknown"

    @classmethod
    def set_profile(cls, profile: str) -> Result:
        """Sets active powerprofile mode.

        Args:
            profile: Target mode ('performance', 'balanced', 'power-saver').

        Returns:
            Result object.
        """
        valid_map = {
            "powersave": "power-saver",
            "power-saver": "power-saver",
            "low": "power-saver",
            "balanced": "balanced",
            "hybrid": "balanced",
            "performance": "performance",
            "full": "performance",
            "gaming": "performance",
        }
        target = valid_map.get(profile.lower(), "balanced")

        if Shell.exists("powerprofilesctl"):
            res = Shell.run(["powerprofilesctl", "set", target], use_shell=False)
            if res.success:
                return Result(
                    success=True,
                    message=f"System power-profiles-daemon set to '{target}'",
                )
            return Result(
                success=False,
                message=f"Failed setting power-profiles-daemon to '{target}': {res.stderr}",
            )

        if Shell.exists("powerctl"):
            res = Shell.run(["powerctl", "set", target], use_shell=False)
            if res.success:
                return Result(
                    success=True,
                    message=f"System powerctl set to '{target}'",
                )

        return Result(
            success=False,
            message="Neither powerprofilesctl nor powerctl found on host system",
        )
