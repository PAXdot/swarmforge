from datetime import datetime, timedelta
from typing import Union

def now() -> datetime:
    """Return current datetime with microsecond resolution."""
    return datetime.utcnow().replace(microsecond=0)

def from_timestamp(timestamp: Union[int, float]) -> datetime:
    """Convert Unix timestamp (float or int) to datetime."""
    return datetime.fromtimestamp(timestamp)

def to_timestamp(dt: datetime) -> float:
    """Convert datetime to Unix timestamp with microsecond resolution."""
    return dt.timestamp() + dt.microsecond / 1_000_000

def ago(seconds: int) -> datetime:
    """Return datetime for a given number of seconds ago."""
    return now() - timedelta(seconds=seconds)
