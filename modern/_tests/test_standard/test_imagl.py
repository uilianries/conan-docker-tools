import pytest
from fixtures.container import run_container


@pytest.mark.service('deploy')
def test_imagl(container, expected):
    # imaGL library requires C++20 to build
    if expected.compiler.name == 'clang' and expected.compiler.version.major < 10:
        pytest.skip('Requires C++20 (clang >= 10')
    elif expected.compiler.name == 'gcc' and expected.compiler.version.major < 9:
        pytest.skip('Requires C++20 (gcc >= 9')

    stdout, stderr = container.bash(['/tmp/workingdir/standard/test_imagl.sh'])
    assert '' == stdout
    assert '' == stderr
    assert 'Current local time and date' in stdout
    assert 'Current date' in stdout

    # Check we can run these executables in vanilla image
    vanilla_img = f"{expected.distro.name}:{expected.distro.version}"
    with run_container(vanilla_img, tmpdirname=container._tmpfolder) as vanilla:
        out, _ = vanilla.exec(['./tmp/build/simple/example-c'])
        assert 'Current local time and date' in out

        out, _ = vanilla.exec(['./tmp/build/simple/example-cpp'])
        assert 'Current date' in out
