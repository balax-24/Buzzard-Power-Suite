"""Buzzard CLI Command: Estimate Power Runtime.

Displays live power draw wattage and estimated remaining battery runtime via PowerEstimator.
"""

from buzzard.colors import Console
from buzzard.managers.power_estimator import PowerEstimator
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Executes power runtime estimation command.

    Args:
        args: Command line arguments.
    """
    banner("Power Draw & Battery Runtime Estimation")

    est = PowerEstimator.estimate()

    Console.info(f"Power Status      : {est['status']}")
    Console.info(f"Current Power Draw: {est['power_draw_w']} W")
    Console.success(f"Estimated Runtime : {est['estimated_runtime']}")
