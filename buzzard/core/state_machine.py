"""Buzzard Profile Application State Machine.

Tracks state transitions during profile application (IDLE -> APPLYING -> VERIFYING -> COMPLETED/FAILED/ROLLBACK).
"""

from enum import Enum, auto
from typing import Callable, List, Optional


class ProfileState(Enum):
    """Profile Application State Enum."""

    IDLE = auto()
    APPLYING = auto()
    VERIFYING = auto()
    COMPLETED = auto()
    FAILED = auto()
    ROLLBACK = auto()


class ProfileStateMachine:
    """State Machine for managing profile execution states."""

    def __init__(self, target_profile: str) -> None:
        """Initializes state machine.

        Args:
            target_profile: Name of target profile.
        """
        self.target_profile = target_profile
        self.state = ProfileState.IDLE
        self.history: List[ProfileState] = [ProfileState.IDLE]
        self._listeners: List[Callable[[ProfileState, ProfileState], None]] = []

    def add_listener(self, callback: Callable[[ProfileState, ProfileState], None]) -> None:
        """Adds state change listener.

        Args:
            callback: Function taking (old_state, new_state).
        """
        self._listeners.append(callback)

    def transition_to(self, new_state: ProfileState) -> None:
        """Transitions state machine to new state.

        Args:
            new_state: Target ProfileState enum value.
        """
        old_state = self.state
        self.state = new_state
        self.history.append(new_state)

        for listener in self._listeners:
            try:
                listener(old_state, new_state)
            except Exception:
                pass

    def is_terminal(self) -> bool:
        """Checks if current state is a terminal state.

        Returns:
            True if state is COMPLETED, FAILED, or ROLLBACK.
        """
        return self.state in (ProfileState.COMPLETED, ProfileState.FAILED, ProfileState.ROLLBACK)
