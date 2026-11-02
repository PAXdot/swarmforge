"""Formatter for human-readable output of consensus between agents and additional metrics."""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence

from swarmforge.consensus_formatter_base import format_decision, format_consensus_summary, format_full_report, format_backoff_policy

class ConsensusFormatter:
    """Produces human-readable strings from consensus data structures.

    Expected input formats:
    - Agent decision: {"agent_id": str, "proposal": str, "vote": Optional[bool], "confidence": float}
    - Consensus result: {"proposal": str, "outcome": str, "vote_counts": {"for": int, "against": int, "abstain": int}, "total_agents": int}
    - Agent state: {"role": str, "active": bool}
    """

    @staticmethod
    def swarm_metrics(agents: Sequence[Dict[str, object]]) -> str:
        """Compute and format swarm-level metrics from a list of agent states.

        Each agent dict must contain at least 'role' and 'active' keys.
        Returns a formatted string with total, active count, inactive count, active ratio,
        and the set of unique roles (cast to string for safety).
        """
        total_agents = len(agents)
        active_agents = [a for a in agents if bool(a.get("active", False))]
        inactive_count = total_agents - len(active_agents)
        active_ratio = len(active_agents) / total_agents if total_agents > 0 else 0.0
        active_roles = {str(a.get("role", "unknown")) for a in active_agents}
        role_list = ", ".join(sorted(active_roles)) if active_roles else "none"
        return (
            f"=== Swarm Metrics ===\n"
            f"Total agents: {total_agents}\n"
            f"Active: {len(active_agents)}  Inactive: {inactive_count}\n"
            f"Active ratio: {active_ratio:.2%}\n"
            f"Active roles: {role_list}"
        )
