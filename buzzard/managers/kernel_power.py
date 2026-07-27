"""Kernel Subsystem Power Optimization Manager.

Applies deep kernel level tweaks to eliminate background timer interrupts,
power down audio codecs, enforce NVMe/PCIe ASPM powersave policies, and extend VM dirty writebacks.

NOTE: Wi-Fi power save is explicitly kept OFF to guarantee maximum internet throughput and minimum latency across all profiles.
"""

from pathlib import Path
from typing import List
from buzzard.core.result import Result
from buzzard.core.shell import Shell


class KernelPowerManager:
    """Deep Kernel Subsystem Power Manager."""

    SYSFS_AUDIO_POWERSAVE = Path("/sys/module/snd_hda_intel/parameters/power_save")
    SYSFS_NMI_WATCHDOG = Path("/proc/sys/kernel/nmi_watchdog")
    SYSFS_DIRTY_WRITEBACK = Path("/proc/sys/vm/dirty_writeback_centisecs")
    SYSFS_LAPTOP_MODE = Path("/proc/sys/vm/laptop_mode")
    SYSFS_ASPM_POLICY = Path("/sys/module/pcie_aspm/parameters/policy")

    @classmethod
    def apply_ultra_power_save(cls) -> List[Result]:
        """Applies deep kernel power savings while preserving full Wi-Fi network performance.

        Returns:
            List of Result objects.
        """
        results: List[Result] = []

        # 1. Audio HDA Intel Power Save (timeout 1s)
        if cls.SYSFS_AUDIO_POWERSAVE.exists():
            res = Shell.write_sysfs(cls.SYSFS_AUDIO_POWERSAVE, "1")
            if res.success:
                results.append(Result(success=True, message="Audio HDA Intel power save activated (1s timeout)"))

        # 2. Disable NMI Watchdog (saves ~10-20 CPU interrupts per second)
        if cls.SYSFS_NMI_WATCHDOG.exists():
            res = Shell.write_sysfs(cls.SYSFS_NMI_WATCHDOG, "0")
            if res.success:
                results.append(Result(success=True, message="NMI Watchdog hardware interrupt timer disabled"))

        # 3. Increase VM Dirty Writeback timeout to 15 seconds (allows SSD/NVMe deep sleep L1.2)
        if cls.SYSFS_DIRTY_WRITEBACK.exists():
            res = Shell.write_sysfs(cls.SYSFS_DIRTY_WRITEBACK, "1500")
            if res.success:
                results.append(Result(success=True, message="VM dirty writeback timer set to 15s"))

        # 4. Enable Kernel Laptop Mode
        if cls.SYSFS_LAPTOP_MODE.exists():
            res = Shell.write_sysfs(cls.SYSFS_LAPTOP_MODE, "5")
            if res.success:
                results.append(Result(success=True, message="Kernel Laptop Mode activated"))

        # 5. Force PCIe ASPM (Active State Power Management) Policy to powersave
        if cls.SYSFS_ASPM_POLICY.exists():
            res = Shell.write_sysfs(cls.SYSFS_ASPM_POLICY, "powersave")
            if res.success:
                results.append(Result(success=True, message="PCIe ASPM policy set to 'powersave'"))

        # 6. Wi-Fi Full Speed Enforcement (Power Save OFF)
        if Shell.exists("iw"):
            iw_res = Shell.run("iw dev")
            if iw_res.success and "Interface " in iw_res.stdout:
                for line in iw_res.stdout.splitlines():
                    if "Interface " in line:
                        iface = line.split()[1]
                        Shell.run(f"iw dev {iface} set power_save off")
                        results.append(Result(success=True, message=f"Wi-Fi full speed enforced on {iface} (power save OFF)"))
                        break

        return results
