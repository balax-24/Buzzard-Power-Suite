"""Buzzard Profile Execution History Service.

Stores and queries structured execution records of all profile applications,
durations, hardware status snapshots, and exit codes.
"""

from datetime import datetime
import json
from typing import Any, Dict, List
from buzzard.core.constants import DATA_DIR, HISTORY_FILE


class HistoryService:
    """Service for persisting and inspecting profile execution history."""

    @classmethod
    def record(
        cls,
        profile: str,
        duration: float,
        status: str,
        battery: int,
        cpu_governor: str,
        gpu: str,
    ) -> None:
        """Records a profile execution event in history.

        Args:
            profile: Name of profile applied.
            duration: Duration of operation in seconds.
            status: Status string (SUCCESS, FAILED).
            battery: Battery percentage at execution time.
            cpu_governor: CPU governor set.
            gpu: GPU mode set.
        """
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "profile": profile,
            "duration_sec": duration,
            "status": status,
            "battery_percent": battery,
            "cpu_governor": cpu_governor,
            "gpu": gpu,
        }

        history = cls.get_history(limit=100)
        history.insert(0, entry)

        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")
        except Exception:
            pass

    @classmethod
    def get_history(cls, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves list of recent profile execution records.

        Args:
            limit: Maximum number of history entries to return.

        Returns:
            List of execution dictionaries.
        """
        if not HISTORY_FILE.exists():
            return []

        try:
            content = HISTORY_FILE.read_text(encoding="utf-8")
            data = json.loads(content)
            if isinstance(data, list):
                return data[:limit]
        except Exception:
            pass

        return []

    @classmethod
    def clear_history(cls) -> None:
        """Clears all stored execution history records."""
        if HISTORY_FILE.exists():
            try:
                HISTORY_FILE.unlink()
            except Exception:
                pass
