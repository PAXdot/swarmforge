from __future__ import annotations
from enum import Enum, auto
from typing import Any, Dict

class SwarmState(Enum):
    INITIALIZING = auto()
    ACTIVE = auto()
    STAGING = auto()
    DORMANT = auto()

class SwarmStateMachine:
    """A finite state machine to manage the swarm's lifecycle."""

    def __init__(self) -> None:
        self._state: SwarmState = SwarmState.INITIALIZING
        self._data: Dict[str, Any] = {}

    @property
    def state(self) -> SwarmState:
        """Get the current state."""
        return self._state

    @property
    def data(self) -> Dict[str, Any]:
        """Get the associated data for the current state."""
        return self._data

    def transit(self, new_state: SwarmState, **kwargs: Any) -> None:
        """Transition to a new state and update associated data if provided."""
        if new_state == self._state:
            return

        self._state = new_state
        self._data = kwargs

    def is_active(self) -> bool:
        """Check if the swarm is active."""
        return self._state == SwarmState.ACTIVE

    def is_dormant(self) -> bool:
        """Check if the swarm is dormant."""
        return self._state == SwarmState.DORMANT
