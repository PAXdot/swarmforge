# src/swarmforge/backoff_validator.py

from typing import Dict, Any, Iterator, ItemsView
from swarmforge.exceptions import InvalidBackoffPolicyError, InvalidSwarmMetricsError
from transitions import Machine

class BackoffValidator:
    def __init__(self):
        self.machine = Machine(
            model=self,
            states=['initial', 'validating_policy', 'policy_invalid', 'validating_metrics', 'valid'],
            transitions=[
                {'trigger': 'start_validation', 'source': 'initial', 'dest': 'validating_policy'},
                {'trigger': 'policy_valid', 'source': 'validating_policy', 'dest': 'validating_metrics'},
                {'trigger': 'policy_invalid', 'source': 'validating_policy', 'dest': 'policy_invalid'},
                {'trigger': 'metrics_valid', 'source': 'validating_metrics', 'dest': 'valid'},
            ],
            initial='initial'
        )

    def validate_backoff_policy(self, policy: Dict[str, Any]) -> None:
        """Validate backoff policy inputs.

        Raises:
            InvalidBackoffPolicyError: If the policy is invalid.
        """
        if not isinstance(policy, dict):
            raise InvalidBackoffPolicyError("Backoff policy must be a dictionary")
        if not all(isinstance(k, str) for k in policy.keys()):
            raise InvalidBackoffPolicyError("Backoff policy keys must be strings")
        if not all(isinstance(v, (int, float)) for v in policy.values()):
            raise InvalidBackoffPolicyError("Backoff policy values must be numbers")

        if self.machine.state == 'policy_invalid':
            self.machine.set_state('validating_policy')
        self.policy_valid()

    def validate_swarm_metrics(self, metrics: Dict[str, Any]) -> None:
        """Validate swarm-level metrics inputs.

        Raises:
            InvalidSwarmMetricsError: If the metrics are invalid.
        """
        if not isinstance(metrics, dict):
            raise InvalidSwarmMetricsError("Swarm metrics must be a dictionary")
        if not all(isinstance(k, str) for k in metrics.keys()):
            raise InvalidSwarmMetricsError("Swarm metrics keys must be strings")
        if not all(isinstance(v, (int, float, str)) for v in metrics.values()):
            raise InvalidSwarmMetricsError("Swarm metrics values must be numbers or strings")

        self.metrics_valid()

    def policy_items(self) -> Iterator[ItemsView[str, Any]]:
        """Return an iterator over the backoff policy's items."""
        if self.machine.state != 'valid':
            raise InvalidBackoffPolicyError("Policy items can only be accessed in the 'valid' state")
        return self.machine.model.policy.items()

validator = BackoffValidator()
validator.start_validation()
