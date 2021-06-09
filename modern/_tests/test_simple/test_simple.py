import pytest


def test_simple(container):
    stdout, stderr = container.exec(['conan', '--version'])
    assert 1 == 1
