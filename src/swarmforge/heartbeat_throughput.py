from __future__ import annotations

import time
from collections import deque
from typing import Optional
from datetime import datetime

class HeartbeatThroughput:
    """Tracks heartbeat event rate over a sliding time window and detects idle periods.

    Attributes:
        window: Duration of the sliding window in seconds (default 60.0).
        start_time: Timestamp of the oldest heartbeat in the current window.
        idle_threshold: Minimum time between heartbeats to be considered idle (default 1.0).
    """

    def __init__(self, window: float = 60.0, idle_threshold: float = 1.0) -> None:
        if window <= 0.0:
            raise ValueError("window must be positive")
        self.window: float = window
        self.idle_threshold: float = idle_threshold
        self._timestamps: deque[float] = deque()

    def record(self) -> None:
        """Record a heartbeat event at the current monotonic time.

        Also triggers idle detection and optionally clears timestamps if idle.
        """
        current_time = time.monotonic()
        self._trim(current_time)
        self._timestamps.append(current_time)
        self.start_time = self._timestamps[0] if self._timestamps else None

        if self._is_idle(current_time):
            self.reset()

    def rate(self) -> float:
        """Return the current heartbeat rate in events per second.

        Returns 0.0 if no events have been recorded within the window.
        """
        current_time = time.monotonic()
        self._trim(current_time)

        if not self._timestamps:
            return 0.0

        # Calculate elapsed time and rate in one step for improved performance
        elapsed_time = current_time - max(self.start_time, self._timestamps[0])
        return len(self._timestamps) / elapsed_time if elapsed_time > 0 else 0.0

    def _trim(self, now: float) -> None:
        """Remove timestamps older than the sliding window."""
        while self._timestamps and self._timestamps[0] < now - self.window:
            self._timestamps.popleft()

    def _is_idle(self, now: float) -> bool:
        """Check if the swarm has been idle for longer than the threshold."""
        return not self._timestamps or self._timestamps[-1] - self._timestamps[0] >= self.idle_threshold

    def reset(self) -> None:
        """Clear all recorded timestamps and resets idle detection."""
        self._timestamps.clear()
        self.start_time = None

    # ... (other methods remain the same)
