"""Utilities for scheduling and time-based role assignment."""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Optional


@dataclass(frozen=True)
class RoleWindow:
    """A time window during which a role is active."""

    role: str
    start_utc: datetime
    end_utc: datetime


class RoleScheduler:
    """Assign roles based on time windows, with optional rotation."""

    def __init__(
        self,
        windows: Optional[list[RoleWindow]] = None,
        now_fn: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
    ) -> None:
        self._windows = windows or []
        self._now_fn = now_fn
        self._current_role: Optional[str] = None

    def add_window(self, role: str, start_utc: datetime, end_utc: datetime) -> None:
        """Add a role window. Windows must not overlap existing ones."""
        if start_utc >= end_utc:
            raise ValueError("start_utc must be before end_utc")
        for existing in self._windows:
            if start_utc < existing.end_utc and end_utc > existing.start_utc:
                raise ValueError(f"Window overlaps with role '{existing.role}'")
        self._windows.append(RoleWindow(role, start_utc, end_utc))
        self._windows.sort(key=lambda w: w.start_utc)

    def active_role(self) -> Optional[str]:
        """Return the role active at the current simulated time."""
        now = self._now_fn()
        for window in self._windows:
            if window.start_utc <= now < window.end_utc:
                self._current_role = window.role
                return window.role
        self._current_role = None
        return None

    def next_role_change(self) -> Optional[datetime]:
        """Return the next time the active role will change or start."""
        now = self._now_fn()
        for window in self._windows:
            if window.start_utc > now:
                return window.start_utc
            if window.start_utc <= now < window.end_utc:
                return window.end_utc
        return None

    def role_duration_left(self, role: str) -> Optional[float]:
        """Seconds remaining in given role's window; None if not active."""
        now = self._now_fn()
        for window in self._windows:
            if window.role == role and window.start_utc <= now < window.end_utc:
                return (window.end_utc - now).total_seconds()
        return None

    def rotate_if_due(self) -> Optional[str]:
        """Return new role if changed, else current role; None if no role."""
        role = self.active_role()
        if role != self._current_role:
            return role
        return role


def parse_iso_utc(iso_string: str) -> datetime:
    """Parse an ISO 8601 string to an aware UTC datetime."""
    parsed = datetime.fromisoformat(iso_string)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def unix_timestamp(dt: Optional[datetime] = None) -> float:
    """Return Unix timestamp for a datetime (default now)."""
    if dt is None:
        dt = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


def wait_until(role: str, scheduler: RoleScheduler, poll_interval: float = 1.0) -> None:
    """Block until the given role becomes active, using real time."""
    while scheduler.active_role() != role:
        time.sleep(poll_interval)
