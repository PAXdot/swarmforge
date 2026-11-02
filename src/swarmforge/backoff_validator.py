# src/swarmforge/backoff_validator.py

import time
from typing import Dict, Union

class BackoffPolicyValidationError(Exception):
    pass

def validate_backoff_policy(policy: Dict) -> None:
    """Validate the backoff policy format.

    Args:
        policy (Dict): A dictionary representing the backoff policy.

    Raises:
        BackoffPolicyValidationError: If the policy format is invalid.
    """
    if not isinstance(policy, dict) or 'base' not in policy or 'factor' not in policy:
        raise BackoffPolicyValidationError("Invalid backoff policy format. Expected {'base': <int>, 'factor': <float>}")

def calculate_backoff(current_retry: int, policy: Dict) -> Union[float, None]:
    """Calculate the backoff duration based on the current retry count and policy.

    Args:
        current_retry (int): The current retry count.
        policy (Dict): The backoff policy.

    Returns:
        Union[float, None]: The duration to wait before retrying, in seconds. Returns None if policy is invalid.
    """
    validate_backoff_policy(policy)

    base = policy.get('base', 1)
    factor = policy.get('factor', 1.0)

    if current_retry == 0:
        return base

    return base * (factor ** current_retry)

# tests/test_backoff_validator.py

def test_calculate_backoff_valid_policy():
    policy = {'base': 1, 'factor': 2.0}
    assert calculate_backoff(0, policy) == 1
    assert calculate_backoff(1, policy) == 2
    assert calculate_backoff(2, policy) == 4

def test_calculate_backoff_invalid_policy():
    assert calculate_backoff(0, {}) is None
    assert calculate_backoff(0, {'base': 1}) is None
    assert calculate_backoff(0, {'factor': 2.0}) is None

def test_calculate_backoff_agent_not_in_heartbeats():
    policy = {'base': 1, 'factor': 2.0}
    agent = 'agent1'
    heartbeats = {'agent2', 'agent3'}

    try:
        calculate_backoff(0, policy)
    except AgentUnavailableError:
        pass
    else:
        assert False, "Expected AgentUnavailableError"
