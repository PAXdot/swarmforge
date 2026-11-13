from datetime import timedelta
from typing import Optional

class HeartbeatValidator:
    """
    Validates the provided heartbeat parameters and raises an exception if they are invalid.
    """

    def __init__(self, min_interval: timedelta, max_interval: timedelta) -> None:
        """
        Initialize the heartbeat validator.

        :param min_interval: The minimum interval between heartbeats.
        :param max_interval: The maximum interval between heartbeats.
        """
        if min_interval < timedelta.zero or min_interval >= max_interval:
            raise ValueError("Invalid heartbeat interval range")
        self.min_interval = min_interval
        self.max_interval = max_interval

    def validate(
        self, expected_heartbeats: int, actual_heartbeats: Optional[int]
    ) -> None:
        """
        Validate the expected and actual heartbeat counts.

        :param expected_heartbeats: The expected number of heartbeats.
        :param actual_heartbeats: The actual number of heartbeats.
        :raises ValueError: If the validation fails.
        """
        if expected_heartbeats is None and actual_heartbeats is not None:
            raise ValueError("Actual heartbeats can only be provided with expected heartbeats")
        if expected_heartbeats is not None and actual_heartbeats is None:
            raise ValueError("Expected heartbeats can't be provided without actual heartbeats")

        if expected_heartbeats is not None and actual_heartbeats is not None:
            if actual_heartbeats < expected_heartbeats:
                raise ValueError(f"Actual heartbeats count ({actual_heartbeats}) is less than expected ({expected_heartbeats})")
