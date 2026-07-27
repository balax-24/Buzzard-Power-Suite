"""Buzzard CLI Help Menu Generator."""

from buzzard.colors import Color
from buzzard.ui.banner import banner


def run(args: list[str] | None = None) -> None:
    """Prints help menu."""
    banner("Command Help Directory")

    print(f"{Color.BOLD}USAGE:{Color.RESET} buzzard <command> [options]\n")

    commands = [
        ("status", "Show active profile, battery telemetry, and GPU state"),
        ("macmode / ultra", "Apply MacBook-Level Ultra Power Saver profile (~3.5W-5W draw)"),
        ("low", "Apply Low Power Saver profile"),
        ("hybrid", "Apply Hybrid Balanced profile"),
        ("full", "Apply Full Performance profile"),
        ("gaming", "Apply Gaming profile (GPU Boost + 120Hz/144Hz + Turbo)"),
        ("creator", "Apply Creator profile (Balanced CPU/GPU + High Refresh)"),
        ("travel", "Apply Travel Saver profile"),
        ("meeting", "Apply Quiet Meeting profile (Silent Fans + Turbo Off)"),
        ("auto", "Run AI & Workload Adaptive profile auto-switching engine"),
        ("doctor", "Run diagnostic health check on power subsystems"),
        ("list", "List available hardware power profiles"),
        ("history", "View historical power profile switches"),
        ("setup", "Configure system permissions & setup background daemon"),
        ("package", "Generate Linux packages (.deb, PKGBUILD, .spec)"),
        ("gui", "Launch desktop system tray telemetry application"),
    ]

    for cmd, desc in commands:
        print(f"  {Color.YELLOW}buzzard {cmd:<18}{Color.RESET} : {desc}")
    print()
