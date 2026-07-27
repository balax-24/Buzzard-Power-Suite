"""Buzzard CLI Command: History.

Displays profile execution history logs via HistoryService.
"""

from buzzard.colors import Console
from buzzard.services.history_service import HistoryService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Executes profile execution history command.

    Args:
        args: Command line arguments.
    """
    banner("Profile Execution History")

    limit = 10
    if args and args[0].isdigit():
        limit = int(args[0])

    records = HistoryService.get_history(limit=limit)

    if not records:
        Console.info("No profile execution history recorded yet.")
        return

    for idx, rec in enumerate(records, 1):
        status_color = Console.success if rec["status"] == "SUCCESS" else Console.error
        Console.info(f"{idx}. [{rec['timestamp']}] Profile: {rec['profile']} ({rec['duration_sec']}s)")
        status_color(f"   Status: {rec['status']} | Battery: {rec['battery_percent']}% | CPU: {rec['cpu_governor']} | GPU: {rec['gpu']}")
        print("   " + "─" * 50)
