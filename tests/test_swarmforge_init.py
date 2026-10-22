"""Tests for the swarmforge package __init__."""

import swarmforge


def test_version_attribute():
    """__version__ should be a string."""
    assert hasattr(swarmforge, "__version__")
    assert isinstance(swarmforge.__version__, str)


def test_version_value():
    """__version__ should equal 0.1.0."""
    assert swarmforge.__version__ == "0.1.0"


def test_version_components():
    """__version__ should have three numeric components separated by dots."""
    parts = swarmforge.__version__.split(".")
    assert len(parts) == 3
    assert all(p.isdigit() for p in parts)
