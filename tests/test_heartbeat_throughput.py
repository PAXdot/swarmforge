import time
from datetime import datetime, timedelta
from swarmforge.heartbeat_throughput import HeartbeatThroughput

def test_init():
    hbt = HeartbeatThroughput(120.0)
    assert hbt.window == 120.0
    assert hbt.start_time is None

def test_record():
    hbt = HeartbeatThroughput()
    initial_length = len(hbt)
    hbt.record()
    assert len(hbt) == initial_length + 1
    assert hbt.start_time is not None

def test_rate():
    hbt = HeartbeatThroughput(60.0)
    hbt.record()
    time.sleep(1)
    hbt.record()
    assert hbt.rate() == 1.0

def test_rate_no_events():
    hbt = HeartbeatThroughput(60.0)
    assert hbt.rate() == 0.0

def test_rate_zero_window():
    hbt = HeartbeatThroughput(0.0)
    assert hbt.rate() == 0.0

def test_reset():
    hbt = HeartbeatThroughput()
    hbt.record()
    hbt.reset()
    assert not hbt._timestamps
    assert hbt.start_time is None

def test_oldest_youngest_timestamp():
    hbt = HeartbeatThroughput()
    hbt.record()
    time.sleep(1)
    hbt.record()
    assert hbt.oldest_timestamp() < hbt.youngest_timestamp()

def test_oldest_youngest_timestamp_empty():
    hbt = HeartbeatThroughput()
    assert hbt.oldest_timestamp() is None
    assert hbt.youngest_timestamp() is None

def test_trim():
    hbt = HeartbeatThroughput(60.0)
    for _ in range(120):
        hbt.record()
        time.sleep(1)
    assert len(hbt) == 60
    assert hbt.rate() == 1.0

def test_repr():
    hbt = HeartbeatThroughput(60.0)
    hbt.record()
    time.sleep(1)
    hbt.record()
    assert "HeartbeatThroughput(window=60.0, events=2, rate=1.000 Hz, oldest=..." in repr(hbt)
