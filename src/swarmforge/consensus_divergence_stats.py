"""Helper module for calculating and tracking consensus divergence statistics."""
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from statistics import mean, stdev

@dataclass
class ConsensusDivergenceStats:
    """Tracks and calculates divergence statistics between agent consensus values.

    Attributes:
        current_values: Latest consensus values from all agents
        history: Rolling window of previous consensus values for trend analysis
        window_size: Number of previous values to consider for trend metrics
    """

    current_values: Dict[str, float]
    history: List[Dict[str, float]] = None
    window_size: int = 10

    def __init__(self, window_size: int = 10) -> None:
        """Initialize with optional history window size."""
        self.history = []
        self.window_size = window_size

    def update(self, new_values: Dict[str, float]) -> None:
        """Update with new consensus values and maintain history window."""
        self.current_values = new_values
        if len(self.history) >= self.window_size:
            self.history.pop(0)
        self.history.append(new_values.copy())

    def get_global_divergence(self) -> float:
        """Calculate current global divergence across all agents."""
        if not self.current_values:
            return 0.0

        values = list(self.current_values.values())
        return stdev(values) if len(values) > 1 else 0.0

    def get_pairwise_divergences(self) -> Dict[Tuple[str, str], float]:
        """Calculate pairwise divergence between all agent pairs."""
        agents = list(self.current_values.keys())
        divergences: Dict[Tuple[str, str], float] = {}

        for i, agent1 in enumerate(agents):
            for agent2 in agents[i+1:]:
                divergence = abs(self.current_values[agent1] - self.current_values[agent2])
                divergences[(agent1, agent2)] = divergence

        return divergences

    def get_trend_divergence(self) -> float:
        """Calculate trend divergence using historical data."""
        if len(self.history) < 2:
            return 0.0

        # Compare first and last in history
        first = self.history[0]
        last = self.history[-1]

        return self._calculate_divergence_between(first, last)

    def get_max_divergence(self) -> float:
        """Return maximum divergence observed in current history."""
        if not self.history:
            return 0.0

        max_div = 0.0
        for snapshot in self.history[:-1]:
            current_div = self._calculate_divergence_between(snapshot, self.current_values)
            if current_div > max_div:
                max_div = current_div

        return max_div

    def _calculate_divergence_between(self, snapshot1: Dict[str, float],
                                     snapshot2: Dict[str, float]) -> float:
        """Helper to calculate divergence between two snapshots."""
        common_agents = set(snapshot1.keys()) & set(snapshot2.keys())
        if not common_agents:
            return 0.0

        divergences = []
        for agent in common_agents:
            divergences.append(abs(snapshot1[agent] - snapshot2[agent]))

        return mean(divergences) if divergences else 0.0

    def get_quantile_divergence(self, q: float = 0.9) -> float:
        """Calculate q-th quantile of divergence across all historical snapshots."""
        if not self.history:
            return 0.0

        divergences = []
        for snapshot in self.history[:-1]:
            current_div = self._calculate_divergence_between(snapshot, self.current_values)
            divergences.append(current_div)

        return sorted(divergences)[int(len(divergences) * q)] if divergences else 0.0
