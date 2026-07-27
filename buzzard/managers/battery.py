"""Battery & AC Subsystem Manager.

Queries Linux sysfs ACPI power supply subsystem (/sys/class/power_supply)
for capacity, charging state, voltage, current draw, and power status.
"""

from pathlib import Path
from typing import Any, Dict, Optional
from buzzard.core.result import Result
from buzzard.core.shell import Shell


class BatteryManager:
    """Battery Hardware Inspection and Power Supply Manager."""

    SYSFS_POWER_SUPPLY = Path("/sys/class/power_supply")

    @classmethod
    def get_battery_path(cls) -> Optional[Path]:
        """Finds primary battery sysfs directory path.

        Returns:
            Path object to BAT node or None if missing.
        """
        if cls.SYSFS_POWER_SUPPLY.exists():
            for entry in cls.SYSFS_POWER_SUPPLY.iterdir():
                if entry.name.startswith("BAT"):
                    return entry
        return None

    @classmethod
    def get_ac_path(cls) -> Optional[Path]:
        """Finds AC power supply sysfs directory path.

        Returns:
            Path object to AC/ADP node or None.
        """
        if cls.SYSFS_POWER_SUPPLY.exists():
            for entry in cls.SYSFS_POWER_SUPPLY.iterdir():
                if entry.name.startswith("AC") or entry.name.startswith("ADP"):
                    return entry
        return None

    @classmethod
    def _read_node(cls, node_name: str, default: str = "Unknown") -> str:
        """Reads a specific sysfs attribute file from the battery path.

        Args:
            node_name: Name of sysfs file (e.g. capacity, status).
            default: Default string if unreadable.

        Returns:
            Attribute text string or default.
        """
        bat = cls.get_battery_path()
        if bat:
            return Shell.read_sysfs(bat / node_name, default=default)
        return default

    @classmethod
    def percent(cls) -> int:
        """Gets current battery charge percentage.

        Returns:
            Integer percentage 0-100 or -1 if unknown.
        """
        val = cls._read_node("capacity", default="-1")
        if val.isdigit():
            return int(val)
        return -1

    @classmethod
    def status(cls) -> str:
        """Gets charging state (Charging, Discharging, Full, Not charging).

        Returns:
            String battery status.
        """
        return cls._read_node("status", default="Unknown")

    @classmethod
    def is_ac_connected(cls) -> bool:
        """Checks whether laptop is connected to AC wall power adapter.

        Returns:
            True if AC connected, False otherwise.
        """
        ac = cls.get_ac_path()
        if ac:
            val = Shell.read_sysfs(ac / "online", default="0")
            return val == "1"
        return cls.status() in ("Charging", "Full")

    @classmethod
    def is_slow_charger(cls) -> bool:
        """Detects if laptop is connected to a low-power source (powerbank/slow USB charger).

        Returns:
            True if AC is reported connected but battery is still discharging or not charging.
        """
        st = cls.status()
        return cls.is_ac_connected() and st in ("Discharging", "Not charging")

    @classmethod
    def voltage(cls) -> float:
        """Gets current battery voltage in Volts.

        Returns:
            Float voltage level.
        """
        val = cls._read_node("voltage_now", default="0")
        if val.isdigit():
            return round(int(val) / 1_000_000, 2)
        return 0.0

    @classmethod
    def current_power_draw(cls) -> float:
        """Calculates current power draw in Watts.

        Returns:
            Float power draw in Watts.
        """
        p_now = cls._read_node("power_now", default="0")
        if p_now.isdigit():
            return round(int(p_now) / 1_000_000, 2)

        c_now = cls._read_node("current_now", default="0")
        v_now = cls._read_node("voltage_now", default="0")
        if c_now.isdigit() and v_now.isdigit():
            return round((int(c_now) / 1_000_000) * (int(v_now) / 1_000_000), 2)

        return 0.0

    @classmethod
    def health_report(cls) -> Dict[str, Any]:
        """Generates comprehensive battery health diagnostics.

        Returns:
            Dictionary containing capacity, status, design full capacity, current full capacity, health %.
        """
        energy_full = cls._read_node("energy_full", default="0")
        energy_design = cls._read_node("energy_full_design", default="0")

        if energy_full == "0":
            energy_full = cls._read_node("charge_full", default="0")
            energy_design = cls._read_node("charge_full_design", default="0")

        health_pct = 100.0
        if energy_full.isdigit() and energy_design.isdigit():
            ef = int(energy_full)
            ed = int(energy_design)
            if ed > 0:
                health_pct = round((ef / ed) * 100.0, 1)

        return {
            "capacity_percent": cls.percent(),
            "status": cls.status(),
            "ac_connected": cls.is_ac_connected(),
            "is_slow_charger": cls.is_slow_charger(),
            "voltage_v": cls.voltage(),
            "power_draw_w": cls.current_power_draw(),
            "health_percent": health_pct,
            "technology": cls._read_node("technology", default="Li-ion"),
        }

    @classmethod
    def get_info(cls) -> Result:
        """Returns standard Result object with battery metrics payload.

        Returns:
            Result object containing health report dictionary in data field.
        """
        report = cls.health_report()
        msg = f"Battery {report['capacity_percent']}% ({report['status']}), AC Connected: {report['ac_connected']}"
        return Result(
            success=report["capacity_percent"] >= 0,
            message=msg,
            data=report,
        )
