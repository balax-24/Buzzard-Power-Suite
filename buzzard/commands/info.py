"""Buzzard CLI Command: Info.

Displays high-level system information summary via DiagnosticService.
"""

from buzzard.colors import Console
from buzzard.services.diagnostic_service import DiagnosticService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Executes info command.

    Args:
        args: Command line arguments.
    """
    banner("System Summary")

    report = DiagnosticService.report()

    Console.info(f"Vendor     : {report['vendor']}")
    Console.info(f"Model      : {report['product']}")
    Console.info(f"Backend    : {report['vendor_backend']}")
    Console.info(f"Kernel     : {report['kernel']}")
    Console.info(f"Arch       : {report['architecture']}")

    deps_ok = sum(1 for v in report["dependencies"].values() if v)
    total_deps = len(report["dependencies"])
    Console.info(f"Dependencies: {deps_ok}/{total_deps} available")
