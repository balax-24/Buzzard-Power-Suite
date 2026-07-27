"""Result object for hardware manager and service operations.

Every manager and service operation returns a Result object to provide
predictable, structured feedback without silent failures.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(slots=True)
class Result:
    """Standard operation result container across Buzzard Power Suite.

    Attributes:
        success: True if the operation completed successfully, False otherwise.
        message: Human-readable explanation of the operation result.
        stdout: Capture of standard output from underlying system calls.
        stderr: Capture of standard error output from underlying system calls.
        reboot_required: Indicates if a system reboot is required for changes to take effect.
        rollback_available: Indicates if the operation state can be safely rolled back.
        data: Optional dictionary payload containing structured return data.
    """

    success: bool
    message: str = ""
    stdout: str = ""
    stderr: str = ""
    reboot_required: bool = False
    rollback_available: bool = False
    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Result object into a standard dictionary.

        Returns:
            Dictionary representation of the result.
        """
        return {
            "success": self.success,
            "message": self.message,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "reboot_required": self.reboot_required,
            "rollback_available": self.rollback_available,
            "data": self.data,
        }
