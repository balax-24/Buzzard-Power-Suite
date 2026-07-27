"""Buzzard Command Dispatcher.

Parses command line arguments and dynamically dispatches control to the
appropriate command handler in buzzard.commands.
"""

import importlib
from typing import List
from buzzard.ui.banner import banner

COMMAND_ALIASES = {
    "--help": "help",
    "-h": "help",
    "help": "help",
    "--version": "version",
    "-v": "version",
    "version": "version",
    "macmode": "macmode",
    "ultra": "macmode",
}

AVAILABLE_COMMANDS = {
    "help",
    "version",
    "doctor",
    "info",
    "status",
    "battery",
    "low",
    "macmode",
    "ultra",
    "hybrid",
    "full",
    "gaming",
    "pentest",
    "llm",
    "dock",
    "creator",
    "travel",
    "meeting",
    "auto",
    "estimate",
    "benchmark",
    "restore",
    "history",
    "optimize",
    "daemon",
    "setup",
    "package",
    "gui",
}


def dispatch(argv: List[str]) -> None:
    """Dispatches CLI invocation to target command handler.

    Args:
        argv: Command line argument list (excluding executable name).
    """
    raw_cmd = argv[0].lower().strip() if argv else "help"
    command = COMMAND_ALIASES.get(raw_cmd, raw_cmd)

    if command not in AVAILABLE_COMMANDS:
        banner("Error")
        print(f"Unknown command: '{raw_cmd}'")
        print("Run 'buzzard help' to view available commands.")
        return

    try:
        module = importlib.import_module(f"buzzard.commands.{command}")
        module.run(argv[1:])
    except Exception as exc:
        banner("Execution Error")
        print(f"Error executing command '{command}': {exc}")
