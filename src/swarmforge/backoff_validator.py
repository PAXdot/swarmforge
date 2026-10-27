# src/swarmforge/backoff_validator.py

from typing import Dict, Any, NoReturn
from swarmforge.exceptions import InvalidBackoffPolicyError, InvalidSwarmMetricsError

def validate_backoff_policy(policy: Dict[str, Any]) -> None:
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

def validate_swarm_metrics(metrics: Dict[str, Any]) -> None:
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
