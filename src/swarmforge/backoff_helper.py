from time import sleep
from typing import Callable
from swarmforge.backoff_strategy import BackoffStrategy
from swarmforge.backoff_validator import BackoffValidator

class TaskQueueBackoffHelper:
    """Helper class for retry/backoff logic in task queues."""

    def __init__(self, backoff_strategy: BackoffStrategy, backoff_validator: BackoffValidator):
        self._backoff_strategy = backoff_strategy
        self._backoff_validator = backoff_validator

    def retry_on_failure(
        self,
        task: Callable,
        max_retries: int = 5,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
    ) -> None:
        """
        Retry the given task on failure, with exponential backoff.

        :param task: The task to retry.
        :param max_retries: Maximum number of retries (default: 5).
        :param initial_delay: Initial delay between retries (default: 1.0 second).
        :param max_delay: Maximum delay between retries (default: 60.0 seconds).
        """
        num_retries = 0
        delay = initial_delay

        while num_retries < max_retries:
            try:
                task()
                return
            except Exception as e:
                if self._backoff_validator.validate(delay):
                    sleep(delay)
                    delay = self._backoff_strategy.next_backoff(delay)
                    num_retries += 1
                else:
                    raise e

        raise RuntimeError(f"Maximum retries ({max_retries}) exceeded.")
