"""Buzzard Core EventBus Architecture.

Provides an asynchronous/synchronous decoupled pub-sub event bus for framework events
such as profile application, hardware status changes, rollbacks, and alerts.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Type


@dataclass
class Event:
    """Base event payload class."""

    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def name(self) -> str:
        """Returns event class name."""
        return self.__class__.__name__


@dataclass
class ProfileAppliedEvent(Event):
    """Event fired when a power profile is successfully applied."""

    profile_name: str = ""
    duration_sec: float = 0.0
    battery_percent: int = 0
    cpu_governor: str = ""
    gpu_mode: str = ""
    reboot_required: bool = False


@dataclass
class ProfileFailedEvent(Event):
    """Event fired when a profile application fails and triggers rollback."""

    profile_name: str = ""
    error_message: str = ""
    duration_sec: float = 0.0


@dataclass
class StatusChangedEvent(Event):
    """Event fired when system hardware state changes."""

    old_state: Dict[str, Any] = field(default_factory=dict)
    new_state: Dict[str, Any] = field(default_factory=dict)


class EventBus:
    """Centralized Decoupled Event Bus."""

    _subscribers: Dict[Type[Event], List[Callable[[Event], None]]] = {}

    @classmethod
    def subscribe(cls, event_type: Type[Event], handler: Callable[[Event], None]) -> None:
        """Subscribes a listener function to a specific event type.

        Args:
            event_type: Subclass of Event.
            handler: Callable taking event instance.
        """
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = []
        if handler not in cls._subscribers[event_type]:
            cls._subscribers[event_type].append(handler)

    @classmethod
    def unsubscribe(cls, event_type: Type[Event], handler: Callable[[Event], None]) -> None:
        """Unsubscribes a listener function from an event type.

        Args:
            event_type: Subclass of Event.
            handler: Callable taking event instance.
        """
        if event_type in cls._subscribers and handler in cls._subscribers[event_type]:
            cls._subscribers[event_type].remove(handler)

    @classmethod
    def publish(cls, event: Event) -> None:
        """Publishes an event instance to all registered handlers.

        Args:
            event: Event instance.
        """
        event_type = type(event)
        handlers = cls._subscribers.get(event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception:
                pass

    @classmethod
    def clear(cls) -> None:
        """Resets all registered event subscriptions."""
        cls._subscribers.clear()
