"""Format consensus results into a consistent string representation.

Supports nested dictionaries, lists, and primitive types recursively.
"""

from __future__ import annotations

from typing import Any


def _format_value(value: Any, indent: int = 0) -> str:
    """Recursively format a value, handling nested dicts, lists, and primitives."""
    prefix = " " * indent
    if isinstance(value, dict):
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


def format_consensus(consensus: list[dict[str, Any]]) -> str:
    """Format a list of consensus entries into a human-readable string.

    Args:
        consensus: A list of dictionaries, each representing a consensus result.

    Returns:
        A formatted string representation.
    """
    if not consensus:
        return ""

    lines: list[str] = []
    for i, entry in enumerate(consensus):
        lines.append(f"Entry {i}:")
        lines.append(_format_value(entry, indent=2))
    return "\n".join(lines)
