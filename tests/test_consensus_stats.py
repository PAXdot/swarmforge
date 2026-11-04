import pytest
from src.swarmforge.consensus_stats import ConsensusStats
from src.swarmforge.consensus_state_machine import ConsensusStateMachine

# Fixture for creating a list of ConsensusStateMachine objects
@pytest.fixture
def consensus_states():
    return [
        ConsensusStateMachine(current_round=1, proposals=[], consensus_reached=True),
        ConsensusStateMachine(current_round=2, proposals=['a', 'b'], consensus_reached=False),
    ]

# Test initial statistics
def test_initial_stats(consensus_states):
    stats = ConsensusStats(consensus_states)
    assert stats.get_stats() == {
        'consensus_rounds': 0,
        'timeouts_1': 0,
        'proposals_1': 0,
        'consensus_1': 0,
        'timeouts_2': 0,
        'proposals_2': 0,
        'consensus_2': 0,
    }

# Test updating statistics
def test_update_stats(consensus_states):
    stats = ConsensusStats(consensus_states)
    stats.update()
    assert stats.get_stats() == {
        'consensus_rounds': 2,
        'timeouts_1': 0,
        'proposals_1': 0,
        'consensus_1': 1,
        'timeouts_2': 0,
        'proposals_2': 2,
        'consensus_2': 0,
    }

# Test resetting statistics
def test_reset_stats(consensus_states):
    stats = ConsensusStats(consensus_states)
    stats.update()
    stats.reset()
    assert stats.get_stats() == {
        'consensus_rounds': 0,
        'timeouts_1': 0,
        'proposals_1': 0,
        'consensus_1': 0,
        'timeouts_2': 0,
        'proposals_2': 0,
        'consensus_2': 0,
    }
