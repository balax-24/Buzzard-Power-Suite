"""Buzzard Adaptive Power Automation Service.

Provides AI/Workload-driven auto-switching logic that dynamically adapts power profiles
based on active applications (gaming, LLM, creator, meeting) and AC/battery status.
"""

import time
from typing import Tuple
from buzzard.core.logger import Logger
from buzzard.core.workload import WorkloadIntrospector
from buzzard.managers import BatteryManager
from buzzard.services.profile_service import ProfileService

logger = Logger()


class AdaptivePowerService:
    """Adaptive Power Automation Service."""

    _last_switch_time: float = 0.0
    _current_target: str = ""
    MIN_SWITCH_INTERVAL: float = 15.0  # Hysteresis interval in seconds

    @classmethod
    def evaluate_and_apply(cls, force: bool = False) -> Tuple[bool, str]:
        """Evaluates active system workload & battery power state and applies profile if changed.

        Args:
            force: Bypass hysteresis timer if True.

        Returns:
            Tuple of (changed boolean, profile_name string).
        """
        now = time.time()
        if not force and (now - cls._last_switch_time) < cls.MIN_SWITCH_INTERVAL:
            return False, cls._current_target or ProfileService.current()

        ac = BatteryManager.is_ac_connected()
        slow = BatteryManager.is_slow_charger()
        pct = BatteryManager.percent()
        detected_workload = WorkloadIntrospector.detect_workload()

        if detected_workload != "default":
            target = detected_workload
        else:
            if ac and not slow:
                target = "full" if pct > 85 else "hybrid"
            else:
                target = "macmode" if pct <= 50 else "low"

        curr = ProfileService.current()
        if target != curr:
            logger.info(f"Adaptive Engine: Detected workload '{detected_workload}' (AC: {ac}, SlowCharger: {slow}, Battery: {pct}%). Auto-switching '{curr}' -> '{target}'")
            success, _ = ProfileService.apply_profile(target)
            if success:
                cls._last_switch_time = now
                cls._current_target = target
                return True, target

        return False, curr
