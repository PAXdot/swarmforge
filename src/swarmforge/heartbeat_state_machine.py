from enum import Enum, auto
from datetime import datetime, timedelta
from typing import Optional

from swarmforge.timestamp import now

class HeartbeatStatus(Enum):
    ACTIVE = auto()
    INACTIVE = auto()
    DEAD = auto()

class HeartbeatStateMachine:
    """State machine for managing heartbeat status"""

    def __init__(self, heartbeat_interval: timedelta):
        self._heartbeat_interval = heartbeat_interval
        self._last_heartbeat: Optional[datetime] = None
        self._status: HeartbeatStatus = HeartbeatStatus.ACTIVE

    @property
    def status(self) -> HeartbeatStatus:
        return self._status

    def heartbeat(self) -> None:
        """Process a heartbeat and update status"""
        now_ = now()
        if not self._last_heartbeat or now_ - self._last_heartbeat >= self._heartbeat_interval:
            self._status = HeartbeatStatus.ACTIVE
            self._last_heartbeat = now_
        elif self._last_heartbeat and now_ - self._last_heartbeat >= self._heartbeat_interval * 2:
            self._status = HeartbeatStatus.INACTIVE

    def mark_as_dead(self) -> None:
        """Mark the bot as dead"""
        self._status = HeartbeatStatus.DEAD
        self._last_heartbeat = None

    def reset(self) -> None:
        """Reset the state machine"""
        self._last_heartbeat = None
        self._status = HeartbeatStatus.ACTIVE
