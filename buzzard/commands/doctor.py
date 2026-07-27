"""Buzzard CLI Command: Doctor.

Runs system health diagnostics via DiagnosticService and formats report for CLI.
"""

from buzzard.colors import Console
from buzzard.services.diagnostic_service import DiagnosticService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Executes system doctor diagnostic command.

    Args:
        args: Command line arguments.
    """
    banner("System Doctor Diagnostics")

    report = DiagnosticService.report()

    Console.info(f"Vendor Backend : {report['vendor_backend']}")
    Console.info(f"System Vendor  : {report['vendor']}")
    Console.info(f"Product Model  : {report['product']}")
    Console.info(f"BIOS Version   : {report['bios']}")
    Console.info(f"Kernel Release : {report['kernel']}")
    Console.info(f"Architecture   : {report['architecture']}")

    print()
    Console.title("Required Dependencies Check")
    for dep, ok in report["dependencies"].items():
        if ok:
            Console.success(f"  [OK] {dep}")
        else:
            Console.error(f"  [MISSING] {dep}")

    print()
    Console.title("Vendor Capabilities")
    for cap, supported in report["vendor_capabilities"].items():
        state_str = "Supported" if supported else "Unsupported"
        if supported:
            Console.success(f"  {cap}: {state_str}")
        else:
            Console.warning(f"  {cap}: {state_str}")

    print()
    bat = report["battery_health"]
    Console.title("Battery Diagnostics")
    Console.info(f"  Charge level: {bat['capacity_percent']}% ({bat['status']})")
    Console.info(f"  Health: {bat['health_percent']}%")
    Console.info(f"  Power draw: {bat['power_draw_w']}W")

    print()
    if report["is_healthy"]:
        Console.success("System health check passed cleanly. All primary dependencies satisfied!")
    else:
        Console.warning(f"System doctor detected missing dependencies: {', '.join(report['missing_dependencies'])}")
