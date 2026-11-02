"""Helper functions for message bus operations."""

import time
from typing import Any

def create_envelope(sender: str, topic: str, payload: Any) -> dict[str, Any]:
    """Build a standard message envelope with sender, topic, payload and timestamp."""
    if not validate_topic(topic):
        raise ValueError(f"Invalid topic: {topic!r}")
    try:
        return {
            "sender": sender,
            "topic": topic,
            "payload": payload,
            "timestamp": time.time(),
        }
    except Exception as e:
        # Handle any other unexpected exceptions
        raise RuntimeError(f"Failed to create envelope: {e}")

def validate_topic(topic: str) -> bool:
    """Return True if topic is a non-empty string of alphanumerics separated by dots."""
    if not topic:
        return False
    parts = topic.split(".")
    return all(p.isalnum() for p in parts)
