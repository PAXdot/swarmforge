from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Union, Tuple

@dataclass
class ConsensusMetrics:
    total_messages: int = 0
    successful_consensus: int = 0
    failed_consensus: int = 0
    consensus_attempts: Union[List[int], None] = None
    consensus_latency: Union[List[float], None] = None

    def __post_init__(self):
        if self.consensus_attempts is None:
            self.consensus_attempts = []
        if self.consensus_latency is None:
            self.consensus_latency = []

    def record_attempt(self, successful: bool, latency: float) -> None:
        self.total_messages += 1
        if successful:
            self.successful_consensus += 1
        else:
            self.failed_consensus += 1
        self.consensus_attempts.append(1 if successful else 0)
        self.consensus_latency.append(latency)

    def avg_consensus_latency(self) -> float:
        return sum(self.consensus_latency) / len(self.consensus_latency) if self.consensus_latency else 0.0

    def consensus_success_rate(self) -> float:
        return self.successful_consensus / self.total_messages if self.total_messages else 0.0

    def consensus_failure_rate(self) -> float:
        return self.failed_consensus / self.total_messages if self.total_messages else 0.0
