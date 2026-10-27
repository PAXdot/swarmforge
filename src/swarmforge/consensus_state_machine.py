from typing import Callable, Dict, Any
import asyncio

class ConsensusStateMachine:
    """A simple state machine for consensus between agents."""

    def __init__(self, initial_state: str, on_change: Callable[[str, str], None]):
        self.current_state = initial_state
        self.transitions: Dict[str, str] = {}
        self.on_change = on_change

    def add_transition(self, from_state: str, to_state: str) -> None:
        """Add a transition rule from one state to another."""
        self.transitions[from_state] = to_state

    async def process(self, event: str, **kwargs: Any) -> None:
        """Process an event and update the state if a transition is possible."""
        next_state = self.transitions.get(self.current_state, self.current_state)
        if next_state != self.current_state:
            self.current_state = next_state
            self.on_change(self.current_state, event)

    def get_state(self) -> str:
        """Return the current state."""
        return self.current_state
