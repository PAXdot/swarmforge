"""A minimal parser for spawn commands used by the swarmforge toolkit.

Parses a spawn command string into structured arguments:
    spawn <agent_type> [--count <n>] [--role <role>] [--ttl <seconds>]

Raises ValueError for invalid input.
"""

from __future__ import annotations

import shlex
from dataclasses import dataclass, field
from typing import Sequence


@dataclass(frozen=True)
class SpawnCommand:
    """Represents a parsed spawn command."""

    agent_type: str
    count: int = 1
    role: str | None = None
    ttl: int | None = None


def parse_spawn_command(line: str) -> SpawnCommand:
    """Parse a spawn command string into a SpawnCommand dataclass.

    Args:
        line: A command string, e.g. 'spawn worker --count 3 --role processor'.

    Returns:
        A SpawnCommand instance.

    Raises:
        ValueError: If the command is malformed or missing required fields.
    """
    tokens: Sequence[str] = shlex.split(line)
    if not tokens:
        raise ValueError("Empty command")
    if tokens[0] != "spawn":
        raise ValueError(f"Expected 'spawn' keyword, got '{tokens[0]}'")

    if len(tokens) < 2:
        raise ValueError("Missing agent type")

    agent_type: str = tokens[1]
    count: int = 1
    role: str | None = None
    ttl: int | None = None

    i: int = 2
    while i < len(tokens):
        token: str = tokens[i]
        if token == "--count":
            i += 1
            if i >= len(tokens):
                raise ValueError("Missing value for --count")
            try:
                count = int(tokens[i])
                if count < 1:
                    raise ValueError
            except ValueError:
                raise ValueError(f"Invalid --count value: '{tokens[i]}'")
        elif token == "--role":
            i += 1
            if i >= len(tokens):
                raise ValueError("Missing value for --role")
            role = tokens[i]
        elif token == "--ttl":
            i += 1
            if i >= len(tokens):
                raise ValueError("Missing value for --ttl")
            try:
                ttl = int(tokens[i])
                if ttl < 0:
                    raise ValueError
            except ValueError:
                raise ValueError(f"Invalid --ttl value: '{tokens[i]}'")
        else:
            raise ValueError(f"Unknown flag: '{token}'")
        i += 1

    return SpawnCommand(agent_type=agent_type, count=count, role=role, ttl=ttl)
