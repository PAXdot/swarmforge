"""Rate/throughput calculator for heartbeat events in a swarm.

Provides a sliding-window calculator that tracks heartbeat timestamps
and computes events per second (Hz) over a configurable window.
Self-contained, no dependencies beyond the standard library.
"""

from __future__ import annotations

import time
from collections import deque
from typing import Optional
from datetime import datetime

class HeartbeatThroughput:
    """Tracks heartbeat event rate over a sliding time window.

    Attributes:
        window: Duration of the sliding window in seconds (default 60.0).
        start_time: Timestamp of the oldest heartbeat in the current window.
    """

    def __init__(self, window: float = 60.0) -> None:
        if window <= 0.0:
            raise ValueError("window must be positive")
        self.window: float = window
        self._timestamps: deque[float] = deque()

    def record(self) -> None:
        """Record a heartbeat event at the current monotonic time."""
        current_time = time.monotonic()
        self._trim(current_time)
        self._timestamps.append(current_time)
        self.start_time = self._timestamps[0] if self._timestamps else None

    def rate(self) -> float:
        """Return the current heartbeat rate in events per second.

        Returns 0.0 if no events have been recorded within the window.
        """
        current_time = time.monotonic()
        self._trim(current_time)

        if not self._timestamps:
            return 0.0

        # Calculate elapsed time and rate in one step for improved performance
        elapsed_time = current_time - self.start_time
        return len(self._timestamps) / elapsed_time if elapsed_time > 0 else 0.0

    def _trim(self, now: float) -> None:
        """Remove timestamps older than the sliding window."""
        while self._timestamps and self._timestamps[0] < now - self.window:
            self._timestamps.popleft()

    def reset(self) -> None:
        """Clear all recorded timestamps."""
        self._timestamps.clear()
        self.start_time = None

    def oldest_timestamp(self) -> Optional[datetime]:
        """Return the timestamp of the oldest heartbeat in the current window."""
        if not self._timestamps:
            return None
        return datetime.fromtimestamp(self._timestamps[0])

    def youngest_timestamp(self) -> Optional[datetime]:
        """Return the timestamp of the youngest heartbeat in the current window."""
        if not self._timestamps:
            return None
        return datetime.fromtimestamp(self._timestamps[-1])

    def __len__(self) -> int:
        """Return the number of events in the current window."""
        current_time = time.monotonic()
        self._trim(current_time)
        return len(self._timestamps)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(window={self.window}, "
            f"events={len(self)}, rate={self.rate():.3f} Hz, oldest={self.oldest_timestamp()}, youngest={self.youngest_timestamp()})"
        )
