from collections import deque
from time import time
from typing import Deque
from swarmforge.consensus_formatter import ConsensusFormatter, ConsensusMessage

class ConsensusThroughputCalculator:
    """Calculate consensus throughput between agents."""

    def __init__(self, formatter: ConsensusFormatter) -> None:
        self._formatter = formatter
        self._messages: Deque[ConsensusMessage] = deque(maxlen=100)
        self._start_time: float = time()

    def update(self, msg: ConsensusMessage) -> None:
        """Process and add a new consensus message."""
        self._formatter.process_message(msg)
        self._messages.append(msg)

    def throughput(self) -> float:
        """Calculate the consensus messages throughput per second."""
        if not self._messages:
            return 0.0

        elapsed_time = time() - self._start_time
        return len(self._messages) / max(elapsed_time, 1.0)

    def reset(self) -> None:
        """Reset the throughput calculator."""
        self._messages.clear()
        self._start_time = time()
