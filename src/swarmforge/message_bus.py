from __future__ import annotations
from typing import Dict, Callable

class MessageBus:
    def __init__(self):
        self._topics: Dict[str, list[Callable]] = {}

    def subscribe(self, topic: str, callback: Callable) -> None:
        """Subscribe a callback to a specific topic."""
        if topic not in self._topics:
            self._topics[topic] = []
        self._topics[topic].append(callback)

    def publish(self, topic: str, *args, **kwargs) -> None:
        """Publish a message to a topic, calling all subscribed callbacks."""
        if topic in self._topics:
            for callback in self._topics[topic]:
                callback(*args, **kwargs)

    def unsubscribe(self, topic: str, callback: Callable) -> None:
        """Unsubscribe a callback from a specific topic."""
        if topic in self._topics:
            self._topics[topic].remove(callback)
