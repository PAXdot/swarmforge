from swarmforge.swarm_state_machine import SwarmState, SwarmStateMachine

def test_initial_state():
    sm = SwarmStateMachine()
    assert sm.state == SwarmState.INITIALIZING
    assert sm.data == {}

def test_transit_to_active():
    sm = SwarmStateMachine()
    sm.transit(SwarmState.ACTIVE)
    assert sm.state == SwarmState.ACTIVE
    assert sm.data == {}

def test_transit_with_data():
    sm = SwarmStateMachine()
    sm.transit(SwarmState.ACTIVE, some_data="data")
    assert sm.state == SwarmState.ACTIVE
    assert sm.data == {"some_data": "data"}

def test_transit_to_same_state():
    sm = SwarmStateMachine()
    sm.transit(SwarmState.ACTIVE)
    sm.transit(SwarmState.ACTIVE)
    assert sm.state == SwarmState.ACTIVE

def test_is_active():
    sm = SwarmStateMachine()
    sm.transit(SwarmState.ACTIVE)
    assert sm.is_active()
    assert not sm.is_dormant()

def test_is_dormant():
    sm = SwarmStateMachine()
    sm.transit(SwarmState.DORMANT)
    assert not sm.is_active()
    assert sm.is_dormant()
