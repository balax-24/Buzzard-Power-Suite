"""Buzzard CLI Command: Status.

Displays snapshot of active profile and hardware subsystem states via StatusService.
"""

from buzzard.colors import Console
from buzzard.services.status_service import StatusService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Executes system status command.

    Args:
        args: Command line arguments.
    """
    banner("System Power Status")

    data = StatusService.get_status()

    Console.info(f"Active Profile      : {data['profile']}")
    Console.info(f"Previous Profile    : {data['previous_profile']}")
    Console.info(f"Vendor Backend      : {data['vendor_name']}")
    print("━" * 40)
    Console.info(f"GPU Mode            : {data['gpu']}")
    Console.info(f"CPU Governor       : {data['cpu_governor']}")
    Console.info(f"Display Brightness  : {data['brightness_percent']}%")
    Console.info(f"Bluetooth Radio     : {data['bluetooth_status']}")
    Console.info(f"TLP Daemon          : {data['tlp_status']}")
    print("━" * 40)
    Console.info(f"Battery Capacity    : {data['battery_percent']}%")

    if data["is_slow_charger"]:
        Console.warning("Power Source        : USB PowerBank / Slow Charger (Discharging!)")
        Console.warning("  ↳ TIP: Run 'buzzard macmode' to prevent battery drain while on powerbank.")
    elif data["ac_connected"]:
        Console.info("Power Source        : AC Adapter")
    else:
        Console.info("Power Source        : Battery")

    Console.info(f"Charging State      : {data['battery_status']}")
    Console.info(f"Power Draw          : {data['power_draw_w']} W")
    if data["battery_charge_limit"] is not None:
        Console.info(f"Battery Charge Limit: {data['battery_charge_limit']}%")
