"""Display Brightness Hardware Subsystem Manager.

Controls backlight brightness levels via brightnessctl binary or sysfs
backlight interface, returning structured Result objects.
"""

from pathlib import Path
from buzzard.core.result import Result
from buzzard.core.shell import Shell


class BrightnessManager:
    """Screen Backlight Brightness Control Manager."""

    SYSFS_BACKLIGHT = Path("/sys/class/backlight")

    @staticmethod
    def get() -> int:
        """Gets current screen brightness percentage (0-100).

        Returns:
            Integer percentage.
        """
        if Shell.exists("brightnessctl"):
            r = Shell.run("brightnessctl get")
            m = Shell.run("brightnessctl max")
            if r.success and m.success and m.stdout.isdigit() and int(m.stdout) > 0:
                return round((int(r.stdout) / int(m.stdout)) * 100)

        # Fallback to sysfs
        if BrightnessManager.SYSFS_BACKLIGHT.exists():
            for card in BrightnessManager.SYSFS_BACKLIGHT.iterdir():
                cur = Shell.read_sysfs(card / "brightness")
                mx = Shell.read_sysfs(card / "max_brightness")
                if cur.isdigit() and mx.isdigit() and int(mx) > 0:
                    return round((int(cur) / int(mx)) * 100)

        return 50

    @staticmethod
    def set(percent: int) -> Result:
        """Sets screen brightness percentage level.

        Args:
            percent: Brightness percentage target (0-100).

        Returns:
            Result object.
        """
        percent = max(1, min(100, percent))
        curr = BrightnessManager.get()

        if Shell.exists("brightnessctl"):
            res = Shell.run(f"brightnessctl set {percent}%")
            if res.success:
                return Result(
                    success=True,
                    message=f"Brightness set to {percent}%",
                    stdout=res.stdout,
                    rollback_available=True,
                    data={"previous": curr, "current": percent},
                )
            # Try elevated brightnessctl if non-root failed
            res = Shell.run(f"sudo brightnessctl set {percent}%", use_shell=True)
            if res.success:
                return Result(
                    success=True,
                    message=f"Brightness set to {percent}%",
                    stdout=res.stdout,
                    rollback_available=True,
                    data={"previous": curr, "current": percent},
                )

        # Fallback to sysfs direct write
        if BrightnessManager.SYSFS_BACKLIGHT.exists():
            for card in BrightnessManager.SYSFS_BACKLIGHT.iterdir():
                mx = Shell.read_sysfs(card / "max_brightness")
                if mx.isdigit() and int(mx) > 0:
                    target_val = int((percent / 100.0) * int(mx))
                    res = Shell.write_sysfs(card / "brightness", str(target_val))
                    if res.success:
                        return Result(
                            success=True,
                            message=f"Brightness set to {percent}% via sysfs",
                            rollback_available=True,
                            data={"previous": curr, "current": percent},
                        )

        return Result(
            success=False,
            message="No supported brightness control utility found (brightnessctl or sysfs)",
        )
