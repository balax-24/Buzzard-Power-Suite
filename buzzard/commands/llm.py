"""Buzzard CLI Command: LLM Profile.

Applies the declarative LLM workload profile via ProfileService.
"""

from buzzard.colors import Console
from buzzard.services.profile_service import ProfileService
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Applies LLM profile.

    Args:
        args: Command line arguments.
    """
    banner("Applying Profile: LLM Workload")

    success, results = ProfileService.apply_profile("llm")

    for res in results:
        if res.success:
            Console.success(f"  [OK] {res.message}")
        else:
            Console.error(f"  [FAIL] {res.message}")

    if success:
        Console.success("\nLLM workload profile applied successfully.")
    else:
        Console.error("\nFailed to apply LLM profile fully. Rollback executed.")
