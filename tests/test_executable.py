"""Testing for executable."""

import pytest
import l4meta.executable as executable


def test_binary():
    """Test for presence of binary."""
    executable.binary('exiftool')


def test_binary_not_present():
    """Test for binary not present."""
    with pytest.raises(Exception):
        executable.binary('lsa')
