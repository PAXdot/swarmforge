from time import sleep
from typing import Callable, Any, Optional
import json
import pickle

class BackoffStrategy:
    """Retry strategy with exponential backoff and jitter."""

    def __init__(self, max_retries: int = 5, initial: float = 1.0, multiplier: float = 2.0, jitter: float = 0.2):
        self.max_retries = max_retries
        self.initial = initial
        self.multiplier = multiplier
        self.jitter = jitter
        self.retries = 0

    def __call__(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        for attempt in range(1, self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                delay = self._calculate_delay(attempt)
                print(f"Retry {attempt} after {delay:.2f} seconds due to: {e}")
                sleep(delay)
        raise RuntimeError(f"Failed after {self.max_retries} retries with: {args[1] if len(args) > 1 else ''}: {e}")

    def _calculate_delay(self, retry: int) -> float:
        base_delay = self.initial * (self.multiplier ** (retry - 1))
        return base_delay + (base_delay * self.jitter * (2 * retry - 1))

    def reset(self) -> None:
        self.retries = 0

    def serialize(self, format: str = "json") -> str:
        """Serialize the BackoffStrategy object to a string.

        Args:
            format (str, optional): The serialization format. Defaults to "json".

        Returns:
            str: The serialized object as a string.

        Raises:
            NotImplementedError: If the format is not supported.
        """
        if format.lower() == "json":
            return json.dumps(self.__dict__)
        elif format.lower() == "pickle":
            return pickle.dumps(self)
        else:
            raise NotImplementedError(f"Format '{format}' is not supported.")

    @classmethod
    def deserialize(cls, data: str, format: str = "json") -> 'BackoffStrategy':
        """Deserialize a BackoffStrategy object from a string.

        Args:
            data (str): The serialized object as a string.
            format (str, optional): The serialization format. Defaults to "json".

        Returns:
            BackoffStrategy: The deserialized object.
        """
        if format.lower() == "json":
            return cls(**json.loads(data))
        elif format.lower() == "pickle":
            return pickle.loads(data)
        else:
            raise NotImplementedError(f"Format '{format}' is not supported.")
