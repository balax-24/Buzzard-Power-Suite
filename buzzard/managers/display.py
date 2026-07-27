"""Display Hardware Subsystem Manager.

Controls screen brightness level and display refresh rate (60Hz / 120Hz / 144Hz)
using xrandr, kscreen-doctor, or wlr-randr.
"""

from buzzard.core.result import Result
from buzzard.core.shell import Shell
from buzzard.managers.brightness import BrightnessManager


class DisplayManager:
    """Display Refresh Rate and Brightness Manager."""

    @staticmethod
    def set_brightness(percent: int) -> Result:
        """Sets display brightness percentage.

        Args:
            percent: Brightness percentage target (0-100).

        Returns:
            Result object.
        """
        return BrightnessManager.set(percent)

    @staticmethod
    def get_brightness() -> int:
        """Gets display brightness percentage.

        Returns:
            Brightness percentage integer.
        """
        return BrightnessManager.get()

    @staticmethod
    def set_refresh_rate(hz: int) -> Result:
        """Sets display refresh rate in Hz.

        Args:
            hz: Target refresh rate (e.g. 60, 120, 144).

        Returns:
            Result object.
        """
        if Shell.exists("xrandr"):
            res_disp = Shell.run("xrandr --query")
            if res_disp.success and " connected" in res_disp.stdout:
                # Find connected display line
                display_name = ""
                for line in res_disp.stdout.splitlines():
                    if " connected" in line:
                        display_name = line.split()[0]
                        break

                if display_name:
                    res = Shell.run(f"xrandr --output {display_name} --mode 1920x1080 --rate {hz}")
                    if res.success:
                        return Result(
                            success=True,
                            message=f"Display refresh rate set to {hz}Hz on {display_name}",
                            rollback_available=True,
                        )

        if Shell.exists("kscreen-doctor"):
            res = Shell.run(f"kscreen-doctor output.1.mode.{hz}Hz")
            if res.success:
                return Result(
                    success=True,
                    message=f"Display refresh rate set to {hz}Hz via kscreen-doctor",
                    rollback_available=True,
                )

        return Result(
            success=False,
            message=f"Display refresh rate configuration tool not active or {hz}Hz unsupported",
        )
