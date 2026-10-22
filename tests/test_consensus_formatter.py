import pytest

from swarmforge.consensus_formatter import ConsensusFormatter


class TestFormatDecision:
    def test_format_decision_for_vote(self):
        decision = {"agent_id": "agent-1", "proposal": "deploy", "vote": True, "confidence": 0.85}
        expected = "  agent-1: FOR (confidence 85.0%)"
        assert ConsensusFormatter.format_decision(decision) == expected

    def test_format_decision_against_vote(self):
        decision = {"agent_id": "agent-2", "proposal": "deploy", "vote": False, "confidence": 0.4}
        expected = "  agent-2: AGAINST (confidence 40.0%)"
        assert ConsensusFormatter.format_decision(decision) == expected

    def test_format_decision_abstain_vote(self):
        decision = {"agent_id": "agent-3", "proposal": "deploy", "vote": None, "confidence": 0.5}
        expected = "  agent-3: ABSTAIN (confidence 50.0%)"
        assert ConsensusFormatter.format_decision(decision) == expected

    def test_format_decision_missing_fields(self):
        decision = {}
        expected = "  unknown: ABSTAIN (confidence 0.0%)"
        assert ConsensusFormatter.format_decision(decision) == expected


class TestFormatConsensusSummary:
    def test_format_consensus_summary_accepted(self):
        result = {
            "proposal": "deploy-v2",
            "outcome": "accepted",
            "vote_counts": {"for": 5, "against": 2, "abstain": 1},
            "total_agents": 8,
        }
        expected = (
            "=== Consensus Decision: 'deploy-v2' ===\n"
            "Outcome: ACCEPTED\n"
            "Votes: 5 for, 2 against, 1 abstain\n"
            "Total agents: 8"
        )
        assert ConsensusFormatter.format_consensus_summary(result) == expected

    def test_format_consensus_summary_rejected(self):
        result = {
            "proposal": "rollback",
            "outcome": "rejected",
            "vote_counts": {"for": 1, "against": 6, "abstain": 0},
            "total_agents": 7,
        }
        expected = (
            "=== Consensus Decision: 'rollback' ===\n"
            "Outcome: REJECTED\n"
            "Votes: 1 for, 6 against, 0 abstain\n"
            "Total agents: 7"
        )
        assert ConsensusFormatter.format_consensus_summary(result) == expected

    def test_format_consensus_summary_undecided(self):
        result = {
            "proposal": "migration",
            "outcome": "undecided",
            "vote_counts": {"for": 2, "against": 2, "abstain": 1},
            "total_agents": 5,
        }
        expected = (
            "=== Consensus Decision: 'migration' ===\n"
            "Outcome: UNDECIDED\n"
            "Votes: 2 for, 2 against, 1 abstain\n"
            "Total agents: 5"
        )
        assert ConsensusFormatter.format_consensus_summary(result) == expected

    def test_format_consensus_summary_missing_fields(self):
        result = {}
        expected = (
            "=== Consensus Decision: '?' ===\n"
            "Outcome: UNDECIDED\n"
            "Votes: 0 for, 0 against, 0 abstain\n"
            "Total agents: 0"
        )
        assert ConsensusFormatter.format_consensus_summary(result) == expected

    def test_format_consensus_summary_invalid_vote_counts_type(self):
        result = {
            "proposal": "test",
            "outcome": "accepted",
            "vote_counts": "not-a-dict",
            "total_agents": 3,
        }
        expected = (
            "=== Consensus Decision: 'test' ===\n"
            "Outcome: ACCEPTED\n"
            "Votes: 0 for, 0 against, 0 abstain\n"
            "Total agents: 3"
        )
        assert ConsensusFormatter.format_consensus_summary(result) == expected


class TestFormatFullReport:
    def test_format_full_report_typical(self):
        decisions = [
            {"agent_id": "a1", "proposal": "deploy", "vote": True, "confidence": 0.9},
            {"agent_id": "a2", "proposal": "deploy", "vote": False, "confidence": 0.3},
            {"agent_id": "a3", "proposal": "deploy", "vote": None, "confidence": 0.5},
        ]
        result = {
            "proposal": "deploy",
            "outcome": "accepted",
            "vote_counts": {"for": 2, "against": 1, "abstain": 1},
            "total_agents": 4,
        }
        expected = (
            "=== Individual Agent Decisions ===\n"
            "  a1: FOR (confidence 90.0%)\n"
            "  a2: AGAINST (confidence 30.0%)\n"
            "  a3: ABSTAIN (confidence 50.0%)\n"
            "\n"
            "=== Consensus Decision: 'deploy' ===\n"
            "Outcome: ACCEPTED\n"
            "Votes: 2 for, 1 against, 1 abstain\n"
            "Total agents: 4"
        )
        assert ConsensusFormatter.format_full_report(decisions, result) == expected

    def test_format_full_report_empty_decisions(self):
        decisions = []
        result = {
            "proposal": "nothing",
            "outcome": "undecided",
            "vote_counts": {"for": 0, "against": 0, "abstain": 0},
            "total_agents": 0,
        }
        expected = (
            "=== Individual Agent Decisions ===\n"
            "\n"
            "=== Consensus Decision: 'nothing' ===\n"
            "Outcome: UNDECIDED\n"
            "Votes: 0 for, 0 against, 0 abstain\n"
            "Total agents: 0"
        )
        assert ConsensusFormatter.format_full_report(decisions, result) == expected
