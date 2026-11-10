import pytest
from swarmforge.timestamp import format_timestamp, parse_timestamp

def test_format_timestamp():
    assert format_timestamp(None) == "unknown"
    assert format_timestamp(1651689600) == "2022-05-17T00:00:00+00:00"

def test_parse_timestamp():
    assert parse_timestamp("2022-05-17T00:00:00+00:00") == 1651689600
    assert parse_timestamp("2022-05-17T00:00:00") == 1652857600
    assert parse_timestamp("invalid") is None
