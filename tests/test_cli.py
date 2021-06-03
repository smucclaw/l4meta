"""Tests for CLI"""

import pytest


@pytest.fixture
def run(testdir):
    def do_run(*args):
        args = ['l4meta'] + list(args)
        return testdir._run(*args)
    return do_run


def test_read_pdf():
    assert 1 == 1


def test_read_greeting_pdf():
    assert 2 == 2
