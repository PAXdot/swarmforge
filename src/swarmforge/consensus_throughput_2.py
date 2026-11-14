import datetime
from collections import deque
from typing import Any

class InsufficientDataError(Exception):
    """Raised when trying to calculate throughput with insufficient data."""

class ConsensusThroughput:
    """Calculate and track throughput of consensus between agents."""

    def __init__(self, window_size: int = 60):
        """Initialize throughput tracker with a given window size in seconds."""
        self.window_size = window_size
        self.window_start = datetime.datetime.now()
        self.messages = deque(maxlen=window_size)

    def track_message(self, message: Any):
        """Track a new consensus message and calculate current throughput."""
        now = datetime.datetime.now()
        self.messages.append((now, message))
        if now - self.window_start > datetime.timedelta(seconds=self.window_size):
            self.window_start = now

    @property
    def throughput(self) -> float:
        """Return current consensus throughput in messages per second.

        Raises:
            InsufficientDataError: If no messages have been tracked yet.
        """
        if not self.messages:
            raise InsufficientDataError("No messages have been tracked yet.")

        return len(self.messages) / (datetime.datetime.now() - self.window_start).total_seconds()
