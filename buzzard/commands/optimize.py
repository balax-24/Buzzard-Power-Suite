"""Buzzard CLI Command: Optimize.

Invokes explicit system power optimizations (TLP, CPU efficiency, PowerTOP autotune) via OptimizeService.
"""

from buzzard.colors import Console
from buzzard.services.optimize_service import OptimizeService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Executes optimize command.

    Args:
        args: Command line arguments.
    """
    banner("System Power Optimization")

    Console.info("Running safe power optimization pipeline...")
    results = OptimizeService.optimize(enable_powertop=True)

    for res in results:
        if res.success:
            Console.success(f"  [OK] {res.message}")
        else:
            Console.error(f"  [FAIL] {res.message}")

    Console.success("\nOptimization pipeline complete.")
