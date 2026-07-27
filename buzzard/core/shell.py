"""Buzzard Shell Execution Wrapper.

This module provides the sole allowed entry point for executing subprocesses,
interacting with sysfs, and querying binary existence in Linux. No other module
or class in Buzzard is permitted to call subprocess or OS system execution directly.
"""

from dataclasses import dataclass
from pathlib import Path
import shlex
import shutil
import subprocess
from typing import List, Union


@dataclass(slots=True)
class ShellResult:
    """Wrapper container for command line execution output.

    Attributes:
        success: True if the command returned exit code 0.
        stdout: Cleaned standard output string.
        stderr: Cleaned standard error string.
        code: Return code of the command execution.
    """

    success: bool
    stdout: str = ""
    stderr: str = ""
    code: int = 0


class Shell:
    """Centralized Linux Shell Execution Engine.

    Guarantees safe invocation of system utilities, error trapping, and uniform logging inputs.
    """

    @staticmethod
    def run(
        command: Union[str, List[str]],
        timeout: Union[int, None] = 15,
        use_shell: bool = False,
    ) -> ShellResult:
        """Executes a system shell command safely.

        Args:
            command: String command line or argument list.
            timeout: Maximum execution timeout in seconds. Defaults to 15 seconds.
            use_shell: Whether to execute via shell interpreter. Defaults to False.

        Returns:
            ShellResult object containing success status, stdout, stderr, and code.
        """
        try:
            if isinstance(command, str):
                if use_shell:
                    args = command
                else:
                    args = shlex.split(command)
            else:
                args = command

            res = subprocess.run(
                args,
                shell=use_shell if isinstance(command, str) else False,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            return ShellResult(
                success=res.returncode == 0,
                stdout=res.stdout.strip() if res.stdout else "",
                stderr=res.stderr.strip() if res.stderr else "",
                code=res.returncode,
            )
        except subprocess.TimeoutExpired:
            return ShellResult(
                success=False,
                stdout="",
                stderr=f"Command execution timed out after {timeout} seconds",
                code=-1,
            )
        except FileNotFoundError as fnf_err:
            return ShellResult(
                success=False,
                stdout="",
                stderr=f"Executable binary not found: {fnf_err}",
                code=127,
            )
        except Exception as exc:
            return ShellResult(
                success=False,
                stdout="",
                stderr=f"Shell execution error: {exc}",
                code=1,
            )

    @staticmethod
    def exists(binary: str) -> bool:
        """Checks if a binary executable exists in the system PATH.

        Args:
            binary: Name of the executable (e.g., 'prime-select', 'powertop').

        Returns:
            True if available in PATH, False otherwise.
        """
        return shutil.which(binary) is not None

    @staticmethod
    def read_sysfs(path: Union[str, Path], default: str = "") -> str:
        """Safely reads content from a sysfs or procfs node.

        Args:
            path: Absolute path to sysfs file.
            default: Default string return if file reading fails.

        Returns:
            Trimmed content of the file or default.
        """
        try:
            target = Path(path)
            if target.exists() and target.is_file():
                return target.read_text(encoding="utf-8").strip()
        except Exception:
            pass
        return default

    @staticmethod
    def write_sysfs(path: Union[str, Path], value: str) -> ShellResult:
        """Writes a string value into a sysfs node safely.

        Args:
            path: Absolute path to sysfs node.
            value: Value string to write.

        Returns:
            ShellResult indicating success or permission failure.
        """
        target = Path(path)
        if not target.exists():
            return ShellResult(
                success=False,
                stdout="",
                stderr=f"Sysfs node does not exist: {path}",
                code=2,
            )

        # First attempt direct python file write if permissions allow
        try:
            target.write_text(str(value), encoding="utf-8")
            return ShellResult(success=True, stdout=f"Wrote {value} to {path}", code=0)
        except PermissionError:
            # Fall back to elevated tee command safely without full shell pipeline if possible
            return Shell.run(["sudo", "tee", str(target)], timeout=5, use_shell=False)
        except Exception as exc:
            return ShellResult(
                success=False,
                stdout="",
                stderr=f"Failed writing sysfs node {path}: {exc}",
                code=1,
            )
