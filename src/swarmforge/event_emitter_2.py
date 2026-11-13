from __future__ import annotations
from typing import Callable, Dict, List

class EventEmitter:
    """A class for emitting and listening to custom events."""

    def __init__(self):
        self._events: Dict[str, List[Callable]] = {}

    def on(self, event: str, callback: Callable) -> None:
        """Add a callback for a specific event."""
        if event not in self._events:
            self._events[event] = []
        self._events[event].append(callback)

    def emit(self, event: str, *args, **kwargs) -> None:
        """Invoke all callbacks for a specific event."""
        if event in self._events:
            for callback in self._events[event]:
                callback(*args, **kwargs)
