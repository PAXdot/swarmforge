import pytest
from src.swarmforge.scoreboard import Scoreboard

def test_update_score():
    sb = Scoreboard()
    sb.update_score("agent1", 10)
    assert sb.scores == {"agent1": 10}
    sb.update_score("agent1", 20)
    assert sb.scores == {"agent1": 20}

def test_update_scores():
    sb = Scoreboard()
    sb.update_scores({"agent1": 10, "agent2": 20})
    assert sb.scores == {"agent1": 10, "agent2": 20}

def test_calculate_ranks():
    sb = Scoreboard()
    sb.update_scores({"agent1": 10, "agent2": 20, "agent3": 30})
    sb.calculate_ranks()
    assert sb.ranks == ["agent3", "agent2", "agent1"]

def test_get_rank():
    sb = Scoreboard()
    sb.update_scores({"agent1": 10, "agent2": 20, "agent3": 30})
    assert sb.get_rank("agent2") == 2

def test_get_ranks():
    sb = Scoreboard()
    sb.update_scores({"agent1": 10, "agent2": 20, "agent3": 30})
    assert sb.get_ranks() == {"agent1": 3, "agent2": 2, "agent3": 1}

def test_reset():
    sb = Scoreboard()
    sb.update_scores({"agent1": 10, "agent2": 20, "agent3": 30})
    sb.calculate_ranks()
    sb.reset()
    assert sb.scores == {}
    assert sb.ranks == []

def test_get_rank_with_update():
    sb = Scoreboard()
    sb.update_scores({"agent1": 10, "agent2": 20, "agent3": 30})
    assert sb.get_rank("agent2") == 2
    sb.update_score("agent1", 40)
    assert sb.get_rank("agent2") == 3

def test_get_ranks_with_update():
    sb = Scoreboard()
    sb.update_scores({"agent1": 10, "agent2": 20, "agent3": 30})
    assert sb.get_ranks() == {"agent1": 3, "agent2": 2, "agent3": 1}
    sb.update_score("agent1", 40)
    assert sb.get_ranks() == {"agent1": 1, "agent2": 3, "agent3": 2}
