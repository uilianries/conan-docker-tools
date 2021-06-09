import pytest


@pytest.mark.service('deploy')
def test_simple(container):
    stdout, stderr = container.bash(['/tmp/workingdir/simple/test_simple.sh'])
    assert 'Current local time and date' in stdout
    assert 'Current date' in stdout
