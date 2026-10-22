"""Formatter for human-readable output of consensus between agents."""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence


class ConsensusFormatter:
    """Produces human-readable strings from consensus data structures.

    Expected input format for each agent's decision:
        {
            "agent_id": str,
            "proposal": str,
            "vote": Optional[bool],
            "confidence": float,  # 0.0 to 1.0
        }

    Expected consensus result format:
        {
            "proposal": str,
            "outcome": str,  # 'accepted', 'rejected', 'undecided'
            "vote_counts": {"for": int, "against": int, "abstain": int},
            "total_agents": int,
        }
    """

    @staticmethod
    def format_decision(decision: Dict[str, object]) -> str:
        """Format a single agent's decision into a line of text."""
        agent_id = str(decision.get("agent_id", "unknown"))
        vote = decision.get("vote")
        confidence = float(decision.get("confidence", 0.0))
        vote_str = "FOR" if vote is True else "AGAINST" if vote is False else "ABSTAIN"
        return f"  {agent_id}: {vote_str} (confidence {confidence:.1%})"

    @staticmethod
    def format_consensus_summary(result: Dict[str, object]) -> str:
        """Format the final consensus result into a block of text."""
        proposal = str(result.get("proposal", "?"))
        outcome = str(result.get("outcome", "undecided"))
        counts = result.get("vote_counts", {})
        total = int(result.get("total_agents", 0))
        if not isinstance(counts, dict):
            counts = {}
        for_count = int(counts.get("for", 0))
        against_count = int(counts.get("against", 0))
        abstain_count = int(counts.get("abstain", 0))

        lines = [
            f"=== Consensus Decision: '{proposal}' ===",
            f"Outcome: {outcome.upper()}",
            f"Votes: {for_count} for, {against_count} against, {abstain_count} abstain",
            f"Total agents: {total}",
        ]
        return "\n".join(lines)

    @staticmethod
    def format_full_report(
        decisions: Sequence[Dict[str, object]],
        result: Dict[str, object],
    ) -> str:
        """Format a full report including all individual decisions and the summary."""
        parts = ["=== Individual Agent Decisions ==="]
        for decision in decisions:
            parts.append(ConsensusFormatter.format_decision(decision))
        parts.append("")
        parts.append(ConsensusFormatter.format_consensus_summary(result))
        return "\n".join(parts)
