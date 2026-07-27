"""PCIe & USB Power Management Manager.

Controls PCIe runtime power management and USB device autosuspend via sysfs nodes.
"""

from pathlib import Path
from typing import Dict
from buzzard.core.result import Result
from buzzard.core.shell import Shell


class PCIeManager:
    """PCIe Power Management and USB Autosuspend Subsystem Manager."""

    SYSFS_BUS_PCIE = Path("/sys/bus/pci/devices")
    SYSFS_BUS_USB = Path("/sys/bus/usb/devices")

    @classmethod
    def usb_autosuspend_status(cls) -> Dict[str, str]:
        """Queries USB autosuspend power control states.

        Returns:
            Dict of device name to control state ('auto' or 'on').
        """
        states = {}
        if cls.SYSFS_BUS_USB.exists():
            for dev in cls.SYSFS_BUS_USB.iterdir():
                ctrl_node = dev / "power" / "control"
                if ctrl_node.exists():
                    val = Shell.read_sysfs(ctrl_node)
                    states[dev.name] = val
        return states

    @classmethod
    def enable_powersave(cls) -> Result:
        """Enables PCIe runtime power management and USB autosuspend.

        Returns:
            Result object.
        """
        count = 0
        if cls.SYSFS_BUS_PCIE.exists():
            for dev in cls.SYSFS_BUS_PCIE.iterdir():
                ctrl_node = dev / "power" / "control"
                if ctrl_node.exists():
                    Shell.write_sysfs(ctrl_node, "auto")
                    count += 1

        if cls.SYSFS_BUS_USB.exists():
            for dev in cls.SYSFS_BUS_USB.iterdir():
                ctrl_node = dev / "power" / "control"
                if ctrl_node.exists():
                    Shell.write_sysfs(ctrl_node, "auto")
                    count += 1

        return Result(
            success=True,
            message=f"PCIe & USB powersave enabled across {count} devices",
            rollback_available=True,
        )
