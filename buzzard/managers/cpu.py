"""CPU Hardware Subsystem Manager.

Manages CPU scaling governor policies, Energy Performance Preference (EPP),
and Intel Turbo Boost / AMD CPB frequency gating.
"""

from pathlib import Path
from typing import List
from buzzard.core.result import Result
from buzzard.core.shell import Shell


class CPUManager:
    """CPU Governor, EPP, and Turbo Boost Frequency Scaling Manager."""

    SYSFS_CPU0_GOV = Path("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
    SYSFS_AVAIL_GOVS = Path("/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors")
    SYSFS_INTEL_NO_TURBO = Path("/sys/devices/system/cpu/intel_pstate/no_turbo")
    SYSFS_AMD_BOOST = Path("/sys/devices/system/cpu/cpufreq/boost")
    SYSFS_CPU0_EPP = Path("/sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference")

    @staticmethod
    def current() -> str:
        """Queries current scaling governor on core 0.

        Returns:
            Current governor name (e.g. powersave, performance, schedutil, unknown).
        """
        gov = Shell.read_sysfs(CPUManager.SYSFS_CPU0_GOV)
        return gov if gov else "unknown"

    @staticmethod
    def available_governors() -> List[str]:
        """Lists available CPU governors reported by kernel.

        Returns:
            List of governor names.
        """
        avail = Shell.read_sysfs(CPUManager.SYSFS_AVAIL_GOVS)
        if avail:
            return avail.split()
        return ["powersave", "performance"]

    @staticmethod
    def set_governor(governor: str) -> Result:
        """Sets scaling governor across all CPU cores.

        Args:
            governor: Governor name (e.g. powersave, performance).

        Returns:
            Result object.
        """
        governor = governor.lower().strip()
        curr = CPUManager.current()
        if curr == governor:
            return Result(
                success=True,
                message=f"CPU governor is already set to '{governor}'",
            )

        res = Shell.run(f"echo {governor} | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor >/dev/null", use_shell=True)

        if res.success:
            return Result(
                success=True,
                message=f"CPU governor changed to '{governor}' across all cores",
                stdout=res.stdout,
                rollback_available=True,
            )
        return Result(
            success=False,
            message=f"Failed to set CPU governor to '{governor}': {res.stderr}",
            stderr=res.stderr,
        )

    @classmethod
    def set_turbo_boost(cls, enabled: bool) -> Result:
        """Enables or disables CPU Turbo Boost / AMD Core Performance Boost.

        Disabling Turbo Boost prevents high wattage spikes and drops power draw significantly.

        Args:
            enabled: Boolean True to enable, False to disable.

        Returns:
            Result object.
        """
        if cls.SYSFS_INTEL_NO_TURBO.exists():
            val = "0" if enabled else "1"
            res = Shell.write_sysfs(cls.SYSFS_INTEL_NO_TURBO, val)
            status_str = "enabled" if enabled else "disabled (ultra power save)"
            if res.success:
                return Result(
                    success=True,
                    message=f"Intel Turbo Boost {status_str}",
                    rollback_available=True,
                )

        if cls.SYSFS_AMD_BOOST.exists():
            val = "1" if enabled else "0"
            res = Shell.write_sysfs(cls.SYSFS_AMD_BOOST, val)
            status_str = "enabled" if enabled else "disabled"
            if res.success:
                return Result(
                    success=True,
                    message=f"AMD CPB Boost {status_str}",
                    rollback_available=True,
                )

        return Result(
            success=False,
            message="CPU Turbo Boost sysfs node not present",
        )

    @classmethod
    def set_epp(cls, preference: str) -> Result:
        """Sets Energy Performance Preference (EPP) across all cores.

        Args:
            preference: EPP string ('power', 'balance_power', 'balance_performance', 'performance').

        Returns:
            Result object.
        """
        if not cls.SYSFS_CPU0_EPP.exists():
            return Result(
                success=False,
                message="Energy Performance Preference (EPP) sysfs node not supported by CPU driver",
            )

        cmd = f"echo {preference} | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/energy_performance_preference >/dev/null"
        res = Shell.run(cmd, use_shell=True)
        if res.success:
            return Result(
                success=True,
                message=f"CPU Energy Performance Preference set to '{preference}'",
                rollback_available=True,
            )

        return Result(
            success=False,
            message=f"Failed setting CPU EPP to '{preference}': {res.stderr}",
        )

    @staticmethod
    def powersave() -> Result:
        """Applies powersave governor to all CPU cores."""
        return CPUManager.set_governor("powersave")

    @staticmethod
    def performance() -> Result:
        """Applies performance governor to all CPU cores."""
        return CPUManager.set_governor("performance")
