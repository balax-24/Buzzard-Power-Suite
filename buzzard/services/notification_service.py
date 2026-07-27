"""Buzzard Desktop Notification Service.

Sends Linux desktop notifications using notify-send utility and listens to EventBus events.
"""

from buzzard.core.event_bus import EventBus, ProfileAppliedEvent, ProfileFailedEvent
from buzzard.core.shell import Shell


class NotificationService:
    """Service for displaying Linux desktop notifications."""

    _initialized = False

    @classmethod
    def initialize(cls) -> None:
        """Subscribes NotificationService handlers to EventBus events."""
        if cls._initialized:
            return
        EventBus.subscribe(ProfileAppliedEvent, cls._on_profile_applied)
        EventBus.subscribe(ProfileFailedEvent, cls._on_profile_failed)
        cls._initialized = True

    @classmethod
    def send(cls, title: str, message: str, urgency: str = "normal") -> None:
        """Sends a desktop notification via notify-send binary.

        Args:
            title: Notification title string.
            message: Notification body message text.
            urgency: Urgency level ('low', 'normal', 'critical').
        """
        if Shell.exists("notify-send"):
            Shell.run(
                ["notify-send", "-u", urgency, "-a", "Buzzard Power Suite", title, message],
                use_shell=False,
            )

    @classmethod
    def _on_profile_applied(cls, event: ProfileAppliedEvent) -> None:
        msg = f"Profile '{event.profile_name}' active (CPU: {event.cpu_governor}, GPU: {event.gpu_mode})"
        if event.reboot_required:
            msg += " [Reboot Required]"
        cls.send("Buzzard Power Suite", msg, urgency="normal")

    @classmethod
    def _on_profile_failed(cls, event: ProfileFailedEvent) -> None:
        cls.send(
            "Buzzard Power Suite Warning",
            f"Failed applying profile '{event.profile_name}': {event.error_message}. Rollback executed.",
            urgency="critical",
        )


# Initialize EventBus notification listener
NotificationService.initialize()
