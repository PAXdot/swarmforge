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


@dataclass
class RoleAssignmentStats:
    """Statistics about role assignments over the scheduler's lifetime."""

    total_assignments: int = 0
    current_role: Optional[str] = None
    current_role_duration: float = 0.0
    current_role_start: Optional[datetime] = None


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
        self._stats = RoleAssignmentStats()

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
        # Before checking windows, capture elapsed duration of the current role
        if self._current_role is not None and self._stats.current_role_start is not None:
            self._stats.current_role_duration = (
                now - self._stats.current_role_start
            ).total_seconds()

        for window in self._windows:
            if window.start_utc <= now < window.end_utc:
                if window.role != self._current_role:
                    # Transitioning to a new role: stats already hold the previous role's duration
                    self._stats.total_assignments += 1
                    self._stats.current_role = window.role
                    self._stats.current_role_start = now
                    self._stats.current_role_duration = 0.0
                self._current_role = window.role
                return window.role

        # No active window found; preserve duration stats before clearing
        if self._current_role is not None:
            # Keep the final duration in self._stats.current_role_duration
            # before clearing the role
            pass
        self._stats.current_role = None
        self._stats.current_role_start = None
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

    def get_stats(self) -> RoleAssignmentStats:
        """Return a snapshot of current role assignment statistics."""
        now = self._now_fn()
        if self._current_role is not None and self._stats.current_role_start is not None:
            self._stats.current_role_duration = (
                now - self._stats.current_role_start
            ).total_seconds()
        return RoleAssignmentStats(
            total_assignments=self._stats.total_assignments,
            current_role=self._stats.current_role,
            current_role_duration=self._stats.current_role_duration,
            current_role_start=self._stats.current_role_start,
        )


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
