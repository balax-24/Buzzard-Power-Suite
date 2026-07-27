"""Buzzard CLI Command: Battery.

Displays battery health diagnostics and charging limits via StatusService.
"""

from buzzard.colors import Console
from buzzard.services.status_service import StatusService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Executes battery status command.

    Args:
        args: Command line arguments.
    """
    banner("Battery & Power Supply Diagnostics")

    data = StatusService.get_status()

    Console.info(f"Capacity Level      : {data['battery_percent']}%")
    Console.info(f"Charging State      : {data['battery_status']}")
    Console.info(f"Power Source        : {'AC Adapter' if data['ac_connected'] else 'Battery'}")
    Console.info(f"Current Voltage     : {data['voltage_v']} V")
    Console.info(f"Power Draw          : {data['power_draw_w']} W")
    Console.info(f"Health Rating       : {data['battery_health_pct']}%")

    if data["battery_charge_limit"] is not None:
        Console.info(f"Battery Charge Limit: {data['battery_charge_limit']}%")
    else:
        Console.warning("Battery charge threshold control is unsupported on current hardware")
