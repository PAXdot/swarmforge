from typing import Iterator, Tuple

from swarmforge.timestamp import get_timestamp

def spawn_iterator(timeout: float, interval: float) -> Iterator[Tuple[int, float]]:
    """
    Generator yielding timestamps and their difference from the previous one.

    Args:
        timeout (float): Maximum allowed interval between timestamps.
        interval (float): Expected interval between timestamps.

    Yields:
        Tuple[int, float]: Current timestamp and its difference from the previous one.
    """
    prev_timestamp = None
    count = 0

    while True:
        current_timestamp = get_timestamp()
        if prev_timestamp is not None and current_timestamp - prev_timestamp > timeout:
            raise TimeoutError(f"Expected a timestamp within the last {timeout} seconds")
        if prev_timestamp is not None:
            diff = current_timestamp - prev_timestamp
            if diff < interval * 0.9 or diff > interval * 1.1:
                raise ValueError(f"Unexpected timestamp interval: {diff} (expected around {interval})")
        yield count, current_timestamp - prev_timestamp if prev_timestamp is not None else 0
        prev_timestamp = current_timestamp
        count += 1
