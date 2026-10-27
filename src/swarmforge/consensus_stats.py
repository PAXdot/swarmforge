"""Consensus statistics helper for SwarmForge."""

from collections import defaultdict
from typing import Dict, List

from src.swarmforge.consensus_state_machine import ConsensusStateMachine

class ConsensusStats:
    """Calculate and store consensus-related statistics."""

    def __init__(self, states: List[ConsensusStateMachine]):
        """Initialize with a list of consensus state machines."""
        self._states = states
        self._statistics = defaultdict(int)

    def update(self):
        """Update statistics based on the current state of all consensus machines."""
        for state in self._states:
            self._statistics['consensus_rounds'] += 1
            self._statistics[f'timeouts_{state.current_round}'] = (
                self._statistics[f'timeouts_{state.current_round}'] + 1
            )
            self._statistics[f'proposals_{state.current_round}'] = (
                self._statistics[f'proposals_{state.current_round}'] + len(state.proposals)
            )
            self._statistics[f'consensus_{state.current_round}'] = (
                self._statistics[f'consensus_{state.current_round}'] + state.consensus_reached
            )

    def get_stats(self) -> Dict[str, int]:
        """Return the current statistics."""
        return dict(self._statistics)

    def reset(self):
        """Reset the statistics counter."""
        self._statistics = defaultdict(int)
