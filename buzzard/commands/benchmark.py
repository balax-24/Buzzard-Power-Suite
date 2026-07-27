"""Buzzard CLI Command: Benchmark.

Measures power drain rate across power profiles.
"""

from buzzard.colors import Console
from buzzard.services.status_service import StatusService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Executes power benchmark measurement command.

    Args:
        args: Command line arguments.
    """
    banner("Power Draw Benchmark")

    status = StatusService.get_status()
    Console.info(f"Active Profile : {status['profile']}")
    Console.info(f"Power Draw     : {status['power_draw_w']} W")
    Console.info(f"Voltage        : {status['voltage_v']} V")
    Console.info(f"AC Connected   : {status['ac_connected']}")
