"""Rate/throughput calculator for heartbeat events in a swarm.

Provides a sliding-window calculator that tracks heartbeat timestamps
and computes events per second (Hz) over a configurable window.
Self-contained, no dependencies beyond the standard library.
"""

from __future__ import annotations

import time
from collections import deque
from typing import Optional


class HeartbeatThroughput:
    """Tracks heartbeat event rate over a sliding time window.

    Attributes:
        window: Duration of the sliding window in seconds (default 60.0).
    """

    def __init__(self, window: float = 60.0) -> None:
        if window <= 0.0:
            raise ValueError("window must be positive")
        self.window: float = window
        self._timestamps: deque[float] = deque()

    def record(self) -> None:
        """Record a heartbeat event at the current monotonic time."""
        now = time.monotonic()
        self._trim(now)
        self._timestamps.append(now)

    def rate(self) -> float:
        """Return the current heartbeat rate in events per second.

        Returns 0.0 if no events have been recorded within the window.
        """
        now = time.monotonic()
        self._trim(now)
        if not self._timestamps:
            return 0.0
        elapsed = now - self._timestamps[0]
        if elapsed <= 0.0:
            return 0.0
        return len(self._timestamps) / elapsed

    def _trim(self, now: float) -> None:
        """Remove timestamps older than the sliding window."""
        cutoff = now - self.window
        while self._timestamps and self._timestamps[0] < cutoff:
            self._timestamps.popleft()

    def reset(self) -> None:
        """Clear all recorded timestamps."""
        self._timestamps.clear()

    def __len__(self) -> int:
        """Return the number of events in the current window."""
        now = time.monotonic()
        self._trim(now)
        return len(self._timestamps)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(window={self.window}, "
            f"events={len(self)}, rate={self.rate():.3f} Hz)"
        )
