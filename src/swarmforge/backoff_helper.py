from time import sleep, time
from typing import Callable, Optional
from swarmforge.backoff_strategy import BackoffStrategy
from swarmforge.backoff_validator import BackoffValidator

class TaskQueueBackoffHelper:
    """Helper class for retry/backoff logic in task queues."""

    def __init__(
        self, backoff_strategy: BackoffStrategy, backoff_validator: BackoffValidator
    ):
        """
        Initialize the backoff helper with the given strategy and validator.

        :param backoff_strategy: The backoff strategy to use.
        :param backoff_validator: The backoff validator to use.
        """
        self._backoff_strategy = backoff_strategy
        self._backoff_validator = backoff_validator

    def retry_on_failure(
        self,
        task: Callable,
        max_retries: int = 5,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_mult: float = 2.0,
        jitter: float = 0.2,
    ) -> None:
        """
        Retry the given task on failure, with exponential backoff.

        :param task: The task to retry.
        :param max_retries: Maximum number of retries (default: 5).
        :param initial_delay: Initial delay between retries (default: 1.0 second).
        :param max_delay: Maximum delay between retries (default: 60.0 seconds).
        :param backoff_mult: Multiplier for exponential backoff (default: 2.0).
        :param jitter: Jitter factor for adding randomness to backoff (default: 0.2).
        """
        num_retries = 0
        delay = initial_delay
        last_attempt_time: Optional[float] = None

        while num_retries < max_retries:
            try:
                task()
                return
            except Exception as e:
                if last_attempt_time is not None:
                    delay = self._calculate_delay(
                        last_attempt_time, delay, max_delay, backoff_mult, jitter
                    )

                if self._backoff_validator.validate(delay):
                    sleep(delay)
                    last_attempt_time = time()
                    num_retries += 1
                else:
                    raise e

        raise RuntimeError(f"Maximum retries ({max_retries}) exceeded.")

    def _calculate_delay(
        self, last_attempt_time: float, curr_delay: float, max_delay: float, mult: float, jitter: float
    ) -> float:
        """
        Calculate the delay for the next attempt based on exponential backoff.

        :param last_attempt_time: The time of the last attempt.
        :param curr_delay: The current delay.
        :param max_delay: The maximum delay.
        :param mult: The multiplier for exponential backoff.
        :param jitter: The jitter factor for adding randomness.
        :return: The delay for the next attempt.
        """
        delay = curr_delay * mult * (1 + jitter * (random() - 0.5))
        return min(delay, max_delay)
