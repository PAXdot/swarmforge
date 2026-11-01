from datetime import datetime, timedelta
from src.swarmforge.heartbeat import Heartbeats

def test_heartbeats_add():
    hb = Heartbeats(3)
    hb.add("agent1", datetime.now())
    assert len(hb._heartbeats) == 1
    hb.add("agent2", datetime.now())
    assert len(hb._heartbeats) == 2

def test_heartbeats_latest():
    hb = Heartbeats()
    hb.add("agent1", datetime.now() - timedelta(seconds=1))
    hb.add("agent1", datetime.now())
    assert hb.latest("agent1").isoformat() == (datetime.now()).isoformat()

def test_heartbeats_reset():
    hb = Heartbeats(2)
    hb.add("agent1", datetime.now())
    hb.add("agent2", datetime.now())
    hb.reset()
    assert len(hb._heartbeats) == 0

def test_heartbeats_as_millis():
    hb = Heartbeats()
    hb.add("agent1", datetime.now() - timedelta(seconds=1))
    hb.add("agent2", datetime.now())
    assert hb.as_millis() == {"agent1": (datetime.now() - timedelta(seconds=1)).isoformat(), "agent2": datetime.now().isoformat()}

def test_heartbeats_maxlen():
    hb = Heartbeats(2)
    hb.add("agent1", datetime.now())
    hb.add("agent2", datetime.now())
    hb.add("agent3", datetime.now())
    assert len(hb._heartbeats) == 2
    assert "agent1" not in hb.as_millis()
