# src/swarmforge/timestamp.py

from datetime import datetime, timezone
from typing import Optional

def format_timestamp(utc_timestamp: Optional[int]) -> str:
    """
    Format an optional UTC timestamp as an ISO 8601 string.

    :param utc_timestamp: Optional UTC timestamp in seconds since the epoch.
    :return: Formatted timestamp string or "unknown" if timestamp is None.
    """
    if utc_timestamp is None:
        return "unknown"
    return datetime.utcfromtimestamp(utc_timestamp).replace(tzinfo=timezone.utc).isoformat()

def parse_timestamp(timestamp: str) -> Optional[int]:
    """
    Parse an ISO 8601 timestamp string and return it as a UTC timestamp.

    :param timestamp: ISO 8601 timestamp string.
    :return: UTC timestamp in seconds since the epoch or None if parsing fails.
    """
    try:
        dt = datetime.fromisoformat(timestamp).astimezone(timezone.utc)
        return int(dt.timestamp())
    except ValueError:
        return None
