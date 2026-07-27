"""Buzzard System Service Alias.

Provides helper snapshot interface wrapping StatusService and DiagnosticService.
"""

from typing import Any, Dict
from buzzard.services.status_service import StatusService


class SystemService:
    """Service for system snapshots."""

    @staticmethod
    def snapshot() -> Dict[str, Any]:
        """Captures status snapshot of system hardware.

        Returns:
            Dictionary containing hardware states.
        """
        status = StatusService.get_status()
        return {
            "gpu": status["gpu"],
            "cpu": status["cpu_governor"],
            "battery": status["battery_percent"],
            "status": status["battery_status"],
            "bluetooth": status["bluetooth_status"],
            "brightness": status["brightness_percent"],
            "profile": status["profile"],
            "power_draw": status["power_draw_w"],
        }
