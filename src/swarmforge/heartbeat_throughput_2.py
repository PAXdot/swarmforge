from __future__ import annotations
from collections import defaultdict
from datetime import timedelta
from typing import DefaultDict, Dict, List, Optional, Tuple

class HeartbeatThroughputCalculator:
    """
    Calculates the throughput of heartbeats based on their timestamps and intervals.
    """

    def __init__(self, interval: timedelta):
        """
        Initialize the throughput calculator with a heartbeat interval.

        :param interval: The expected interval between heartbeats.
        """
        self.interval = interval
        self._last_heartbeats: DefaultDict[str, List[timedelta]] = defaultdict(list)

    def track_heartbeats(self, agent_id: str, timestamp: timedelta) -> None:
        """
        Track a heartbeat and update the throughput data for the given agent.

        :param agent_id: The ID of the agent that sent the heartbeat.
        :param timestamp: The timestamp of the received heartbeat.
        """
        last_heartbeats = self._last_heartbeats[agent_id]
        last_heartbeats.append(timestamp - last_heartbeats[-1] if last_heartbeats else timestamp)

        # Remove old timestamps to keep only the last N heartbeats
        while len(last_heartbeats) > 10:
            last_heartbeats.pop(0)

    def get_throughput(self, agent_id: Optional[str] = None) -> Dict[str, float]:
        """
        Calculate the throughput of heartbeats for all or a specific agent.

        :param agent_id: The ID of the agent to calculate the throughput for. If None, calculate for all agents.
        :return: A dictionary containing the throughput values for the specified agent or all agents.
        """
        if agent_id is None:
            return {agent: self._calculate_throughput(heartbeats) for agent, heartbeats in self._last_heartbeats.items()}
        else:
            return {agent_id: self._calculate_throughput(self._last_heartbeats.get(agent_id, []))}

    def _calculate_throughput(self, heartbeats: List[timedelta]) -> float:
        """
        Calculate the throughput of heartbeats based on the given timestamps.

        :param heartbeats: A list of timestamps representing the received heartbeats.
        :return: The calculated throughput in heartbeats per second.
        """
        if not heartbeats:
            return 0.0

        total_duration = sum(heartbeats, timedelta(0)).total_seconds()
        num_heartbeats = len(heartbeats)
        return num_heartbeats / total_duration if total_duration > 0 else 0.0
