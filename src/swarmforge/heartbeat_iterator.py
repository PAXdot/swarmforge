"""Iterator/generator for yielding agent heartbeats with optional staleness filter."""

from __future__ import annotations

import time
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class HeartbeatSample:
    """A single heartbeat sample with agent id and timestamp."""

    agent_id: str
    timestamp: float
    metadata: dict[str, Any] | None = None


class HeartbeatIterator:
    """Iterates over a sequence of heartbeat samples, filtering by maximum age.

    Typical usage::

        samples = [HeartbeatSample("a1", time.time()), ...]
        for hb in HeartbeatIterator(samples, max_age_sec=5.0):
            process(hb)
    """

    def __init__(
        self,
        samples: list[HeartbeatSample],
        max_age_sec: float | None = None,
    ) -> None:
        if max_age_sec is not None and max_age_sec < 0:
            raise ValueError("max_age_sec must be non-negative")
        self._samples = list(samples)
        self._max_age = max_age_sec
        self._index = 0

    def __iter__(self) -> Iterator[HeartbeatSample]:
        return self

    def __next__(self) -> HeartbeatSample:
        now = time.monotonic()
        while self._index < len(self._samples):
            sample = self._samples[self._index]
            self._index += 1
            if self._max_age is None or (now - sample.timestamp) <= self._max_age:
                return sample
        raise StopIteration

    @property
    def remaining(self) -> int:
        """Number of samples not yet consumed."""
        return len(self._samples) - self._index


def heartbeat_generator(
    samples: list[HeartbeatSample],
    max_age_sec: float | None = None,
) -> Iterator[HeartbeatSample]:
    """Generator yielding fresh heartbeat samples, skipping stale ones.

    Args:
        samples: Sequence of heartbeat samples.
        max_age_sec: Maximum age in seconds; ``None`` means no limit.

    Yields:
        HeartbeatSample instances that are not older than ``max_age_sec``.
    """
    if max_age_sec is not None and max_age_sec < 0:
        raise ValueError("max_age_sec must be non-negative")

    now = time.monotonic()
    for sample in samples:
        if max_age_sec is None or (now - sample.timestamp) <= max_age_sec:
            yield sample
