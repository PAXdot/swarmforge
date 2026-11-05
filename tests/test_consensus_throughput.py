# tests/test_consensus_throughput.py

from datetime import timedelta
from time import sleep
from unittest.mock import Mock

import pytest
from swarmforge.consensus_formatter import ConsensusFormatter, ConsensusMessage
from swarmforge.consensus_throughput import ConsensusThroughputCalculator

def test_throughput_empty():
    """Test throughput calculation when no messages are added."""
    calculator = ConsensusThroughputCalculator(Mock(spec=ConsensusFormatter))
    assert calculator.throughput() == 0.0

def test_throughput():
    """Test throughput calculation with a single message."""
    formatter = Mock(spec=ConsensusFormatter)
    calculator = ConsensusThroughputCalculator(formatter)

    msg = ConsensusMessage("agent1", "agent2", "data")
    calculator.update(msg)

    assert calculator.throughput() > 0.0

def test_throughput_many_messages():
    """Test throughput calculation with multiple messages."""
    formatter = Mock(spec=ConsensusFormatter)
    calculator = ConsensusThroughputCalculator(formatter)

    for i in range(1000):
        msg = ConsensusMessage(f"agent{i}", f"agent{i+1}", f"data{i}")
        calculator.update(msg)

        if i < 99:
            assert calculator.throughput() < 100.0
        else:
            sleep(1)  # Let some time pass for the throughput calculation

    assert calculator.throughput() > 900.0

def test_reset():
    """Test resetting the throughput calculator."""
    formatter = Mock(spec=ConsensusFormatter)
    calculator = ConsensusThroughputCalculator(formatter)

    calculator.update(ConsensusMessage("agent1", "agent2", "data"))
    calculator.reset()

    assert calculator.throughput() == 0.0
