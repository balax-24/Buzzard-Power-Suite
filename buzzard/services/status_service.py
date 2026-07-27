"""Buzzard System Status Service.

Gathers hardware status snapshots across GPU, CPU, Battery, Brightness,
Bluetooth, TLP daemon, and active profile detection.
"""

from typing import Any, Dict
from buzzard.managers import (
    BatteryManager,
    BluetoothManager,
    BrightnessManager,
    CPUManager,
    GPUManager,
    TLPManager,
    VendorManager,
)
from buzzard.services.profile_service import ProfileService


class StatusService:
    """Service for querying hardware subsystem status snapshots."""

    @classmethod
    def get_status(cls) -> Dict[str, Any]:
        """Gathers snapshot of system power state across all subsystems.

        Returns:
            Dictionary containing hardware status details.
        """
        active_profile = ProfileService.current()
        previous_profile = ProfileService.previous()
        bat_report = BatteryManager.health_report()

        return {
            "profile": active_profile,
            "previous_profile": previous_profile,
            "gpu": GPUManager.current(),
            "cpu_governor": CPUManager.current(),
            "available_governors": CPUManager.available_governors(),
            "brightness_percent": BrightnessManager.get(),
            "bluetooth_status": BluetoothManager.status(),
            "tlp_status": TLPManager.status(),
            "vendor_name": VendorManager.vendor_name(),
            "vendor_capabilities": VendorManager.capabilities(),
            "battery_charge_limit": VendorManager.get_charge_limit(),
            "battery_percent": bat_report["capacity_percent"],
            "battery_status": bat_report["status"],
            "ac_connected": bat_report["ac_connected"],
            "is_slow_charger": bat_report.get("is_slow_charger", False),
            "voltage_v": bat_report["voltage_v"],
            "power_draw_w": bat_report["power_draw_w"],
            "battery_health_pct": bat_report["health_percent"],
        }
