from time import sleep
from typing import Callable, Any, Optional

class BackoffStrategy:
    """Retry strategy with exponential backoff and jitter."""

    def __init__(self, max_retries: int = 5, initial: float = 1.0, multiplier: float = 2.0, jitter: float = 0.2):
        self.max_retries = max_retries
        self.initial = initial
        self.multiplier = multiplier
        self.jitter = jitter
        self.retries = 0

    def __call__(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        while self.retries < self.max_retries:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                sleep(self._calculate_delay(self.retries))
                self.retries += 1
        raise RuntimeError(f"Max retries exceeded with url '{args[1]}': {e}")

    def _calculate_delay(self, retry: int) -> float:
        base_delay = self.initial * (self.multiplier ** retry)
        return base_delay + (base_delay * self.jitter * (2 * retry - 1))

    def reset(self) -> None:
        self.retries = 0
