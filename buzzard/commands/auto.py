"""Buzzard CLI Command: Auto Adaptive Profile Switcher.

Auto-selects power profile based on active application workloads (gaming, LLM, creator, meeting)
and battery/AC power state.
"""

from buzzard.colors import Console
from buzzard.services.adaptive_service import AdaptivePowerService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Executes auto adaptive profile selector command.

    Args:
        args: Command line arguments.
    """
    banner("Auto Adaptive Profile Evaluation")

    Console.info("Introspecting active process table and power state...")
    changed, active_profile = AdaptivePowerService.evaluate_and_apply(force=True)

    if changed:
        Console.success(f"\nAdaptive engine auto-switched profile to '{active_profile.upper()}'!")
    else:
        Console.info(f"\nSystem active profile '{active_profile.upper()}' is optimal for current workload.")
