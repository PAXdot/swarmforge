from __future__ import annotations

from typing import Any, Optional, List, Dict, Union, Callable

TaskQueue = Dict[str, Any]  # Task queue format: {"task_id": {"arguments": ..., "priority": ..., ...}}

def _format_value(value: Optional[Union[dict, list, Any]], indent: int = 0) -> str:
    """Recursively format a value, handling nested dicts, lists, None, and primitives."""
    prefix = " " * indent
    if value is None:
        return f"{prefix}- None"
    elif isinstance(value, dict):
        items = []
        for key, val in value.items():
            formatted_val = _format_value(val, indent + 2)
            items.append(f"{prefix}  {key}: {formatted_val}")
        return "\n".join(items)
    elif isinstance(value, list):
        items = []
        for item in value:
            formatted_item = _format_value(item, indent + 2)
            items.append(f"{prefix}- {formatted_item}")
        return "\n".join(items)
    else:
        return str(value)

def format_consensus(consensus: List[Optional[TaskQueue]], stats_func: Callable[[List[Optional[TaskQueue]]], Dict[str, Any]]) -> str:
    """Format a list of consensus entries for task queues into a human-readable string.

    Args:
        consensus: A list of TaskQueue dictionaries, each representing a consensus result.
            Can contain None values.
        stats_func: A function that takes the consensus list and returns a dictionary
            containing statistics about backoff policies and swarm-level metrics.

    Returns:
        A formatted string representation.
    """
    if not consensus:
        return ""

    lines: list[str] = []
    for i, entry in enumerate(consensus):
        if entry is not None:  # Skip None values
            lines.append(f"Task Queue {i}:")
            lines.append(_format_value(entry.get("arguments", {}), indent=2))
            lines.append(f"{prefix}Priority: {entry['priority']}")
    lines.extend(f"{key}: {value}" for key, value in stats_func(consensus).items())
    return "\n".join(lines)
