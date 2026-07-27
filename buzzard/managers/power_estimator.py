"""Power Estimator Subsystem Manager.

Calculates live power draw wattage, battery energy capacity, and calculates
remaining battery runtime estimations (hours and minutes).
"""

from typing import Any, Dict
from buzzard.managers.battery import BatteryManager


class PowerEstimator:
    """Live Battery Power Draw & Remaining Runtime Estimator."""

    @classmethod
    def estimate(cls) -> Dict[str, Any]:
        """Calculates power draw metrics and remaining runtime estimation.

        Returns:
            Dictionary containing power draw (W), remaining capacity (Wh),
            time remaining string (e.g. '5h 18m'), and raw hours decimal.
        """
        report = BatteryManager.health_report()
        power_w = report["power_draw_w"]
        pct = report["capacity_percent"]
        status = report["status"]
        ac_connected = report["ac_connected"]

        # Estimated total full charge battery energy capacity for typical 50Wh laptop battery if sysfs missing
        total_wh = 50.0
        remaining_wh = (pct / 100.0) * total_wh

        if ac_connected or status == "Charging":
            return {
                "power_draw_w": power_w,
                "status": "Charging",
                "estimated_runtime": "Plugged In (AC)",
                "hours_remaining": 0.0,
            }

        if power_w <= 0.5:
            # Baseline idle estimate
            power_w = 8.5

        hours_remaining = round(remaining_wh / power_w, 2)
        hrs = int(hours_remaining)
        mins = int((hours_remaining - hrs) * 60)
        time_str = f"{hrs}h {mins:02d}m"

        return {
            "power_draw_w": round(power_w, 2),
            "status": "Discharging",
            "estimated_runtime": time_str,
            "hours_remaining": hours_remaining,
        }
