"""Buzzard Logging Module.

Provides centralized file logging for system operations, profile switching events,
warnings, and diagnostic errors.
"""

from datetime import datetime
from pathlib import Path
from typing import Union
from buzzard.core.constants import LOG_FILE, LOG_DIR


class Logger:
    """Central Logger class for Buzzard Power Suite."""

    def __init__(self, log_path: Union[Path, None] = None):
        """Initializes logger destination directory and file.

        Args:
            log_path: Optional custom path to log file. Defaults to ~/.local/share/buzzard/logs/buzzard.log.
        """
        self.log_file = log_path or LOG_FILE
        self._ensure_log_dir()

    def _ensure_log_dir(self) -> None:
        """Ensures that log directory exists on disk."""
        try:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    def write(self, level: str, message: str) -> None:
        """Writes a formatted entry to the log file.

        Args:
            level: Log level indicator (e.g. INFO, WARNING, ERROR).
            message: Text message to write.
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{now}] [{level.upper()}] {message}\n"
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception:
            pass

    def info(self, message: str) -> None:
        """Writes an INFO level message.

        Args:
            message: Information log message.
        """
        self.write("INFO", message)

    def warning(self, message: str) -> None:
        """Writes a WARNING level message.

        Args:
            message: Warning log message.
        """
        self.write("WARNING", message)

    def error(self, message: str) -> None:
        """Writes an ERROR level message.

        Args:
            message: Error log message.
        """
        self.write("ERROR", message)

    def debug(self, message: str) -> None:
        """Writes a DEBUG level message.

        Args:
            message: Debug log message.
        """
        self.write("DEBUG", message)


# Global default logger instance
default_logger = Logger()
