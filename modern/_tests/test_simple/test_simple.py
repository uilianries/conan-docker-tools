import pytest
from fixtures.container import DockerContainer


@pytest.mark.service('deploy')
def test_simple(container, expected):
    stdout, stderr = container.bash(['/tmp/workingdir/simple/test_simple.sh'])
    assert 'Current local time and date' in stdout
    assert 'Current date' in stdout

    # Check we can run these executables in vanilla image
    vanilla_img = f"ubuntu:{expected.distro.name}"
    vanilla = DockerContainer(image=vanilla_img, tmpfolder=container._tmpfolder)
    try:
        vanilla.run()
        out, _ = vanilla.exec(['./tmp/build/simple/example-c'])
        assert 'Current local time and date' in out

        out, _ = vanilla.exec(['./tmp/build/simple/example-cpp'])
        assert 'Current date' in out
    finally:
        vanilla.stop()
