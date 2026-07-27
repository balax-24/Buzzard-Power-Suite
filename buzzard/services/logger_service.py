"""Buzzard Logger Service.

Appends log records to centralized system log.
"""

from buzzard.core.logger import Logger

_logger = Logger()


class LoggerService:
    """Service wrapper for logging system events."""

    @classmethod
    def write(cls, message: str, level: str = "INFO") -> None:
        """Writes message to central log file.

        Args:
            message: Text message string.
            level: Log level string (INFO, WARNING, ERROR).
        """
        _logger.write(level, message)
