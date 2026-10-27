from collections import deque
from typing import Dict, Optional
from datetime import datetime
from .timestamp import timestamp_millis

Heartbeat = Dict[str, datetime]

class Heartbeats:
    def __init__(self, capacity: int = 10):
        self._heartbeats: deque[Heartbeat] = deque(maxlen=capacity)

    def add(self, agent_id: str, timestamp: datetime) -> None:
        self._heartbeats.append({agent_id: timestamp})

    def latest(self, agent_id: str) -> Optional[datetime]:
        return next((t for t in self._heartbeats if agent_id in t), None).get(agent_id)

    def reset(self) -> None:
        self._heartbeats.clear()

    def as_millis(self) -> Dict[str, Optional[int]]:
        return {agent_id: (t.isoformat() if t else None) for t in self._heartbeats for agent_id, t in t.items()}
