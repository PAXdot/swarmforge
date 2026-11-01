from __future__ import annotations
from typing import Dict, List
from swarmforge.timestamp import Timestamp
from swarmforge.role_scheduler import RoleScheduler

class Scoreboard:
    """
    A class to manage scoring and ranking of autonomous agents in a swarm.
    """

    def __init__(self):
        self.scores: Dict[str, int] = {}
        self.ranks: List[str] = []

    def update_score(self, agent_id: str, score: int):
        """
        Update the score of an agent.

        :param agent_id: The ID of the agent.
        :param score: The new score of the agent.
        """
        self.scores[agent_id] = score

    def update_scores(self, scores: Dict[str, int]):
        """
        Update scores of multiple agents at once.

        :param scores: A dictionary with agent IDs as keys and scores as values.
        """
        self.scores.update(scores)

    def calculate_ranks(self):
        """
        Calculate and update the ranks of all agents based on their scores.
        """
        sorted_agents = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        self.ranks = [agent_id for agent_id, _ in sorted_agents]

    def get_rank(self, agent_id: str) -> int:
        """
        Get the rank of an agent.

        :param agent_id: The ID of the agent.
        :return: The rank of the agent.
        """
        self.calculate_ranks()
        return self.ranks.index(agent_id) + 1

    def get_ranks(self) -> Dict[str, int]:
        """
        Get the ranks of all agents.

        :return: A dictionary with agent IDs as keys and ranks as values.
        """
        self.calculate_ranks()
        return {agent_id: rank for rank, (agent_id, _) in enumerate(self.scores.items(), start=1)}

    def reset(self):
        """
        Reset the scores and ranks of all agents.
        """
        self.scores = {}
        self.ranks = []

class AgentPerformanceMetric:
    """
    A class to monitor and calculate performance metrics for autonomous agents.
    """

    def __init__(self, role_scheduler: RoleScheduler, heartbeat_interval: Timestamp):
        self.role_scheduler = role_scheduler
        self.heartbeat_interval = heartbeat_interval
        self.scores = Scoreboard()
        self.last_heartbeats: Dict[str, Timestamp] = {}

    def update_heartbeats(self, agent_id: str, timestamp: Timestamp):
        """
        Update the last heartbeat timestamp of an agent.

        :param agent_id: The ID of the agent.
        :param timestamp: The timestamp of the agent's heartbeat.
        """
        self.last_heartbeats[agent_id] = timestamp

    def calculate_scores(self):
        """
        Calculate the scores of all agents based on their heartbeats and scheduled roles.
        """
        for agent_id, role in self.role_scheduler.get_current_roles().items():
            if agent_id not in self.last_heartbeats:
                self.scores.update_score(agent_id, 0)
                continue

            heartbeat_duration = Timestamp(self.last_heartbeats[agent_id])
            score = int(heartbeat_duration / self.heartbeat_interval) * role.get_score_multiplier()

            self.scores.update_score(agent_id, score)
            del self.last_heartbeats[agent_id]
