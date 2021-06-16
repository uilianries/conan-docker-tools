import pytest
from fixtures.container import run_container


@pytest.mark.compiler('gcc')
@pytest.mark.service('deploy')
def test_gcc_conan(container, expected):
    build_directory = '/tmp/build/gcc_conan'
    # Compile the project
    with container.working_dir(build_directory):
        container.exec(['conan', 'create', '/tmp/workingdir/gcc_conan/conanfile.py', 'foo/0.1@user/testing', '--build'])
        container.exec(['conan', 'install', 'foo/0.1@user/testing', '-g', 'deploy'])

        out, err = container.exec(['./bin/foobar'])
        assert 'Current local time and date' in out, f"out: '{out}' err: '{err}'"
        out, err = container.exec(['./bin/foobar_c'])
        assert 'Current date' in out, f"out: '{out}' err: '{err}'"

        out, err = container.exec(['ldd', 'bin/foobar'])
        assert 'libstdc++.so.6 => /usr/local/lib64/libstdc++.so.6' in out, f"out: '{out}' err: '{err}'"
        assert 'libgcc_s.so.1 => /usr/local/lib64/libgcc_s.so.1' in out, f"out: '{out}' err: '{err}'"

        out, err = container.exec(['ldd', 'bin/foobar_c'])
        assert 'libstdc++.so.6 => /usr/local/lib64/libstdc++.so.6' in out, f"out: '{out}' err: '{err}'"
        assert 'libgcc_s.so.1 => /usr/local/lib64/libgcc_s.so.1' in out, f"out: '{out}' err: '{err}'"

    # Check we can run these executables in vanilla image
    vanilla_img = f"{expected.distro.name}:{expected.distro.version}"
    with run_container(vanilla_img, tmpdirname=container._tmpfolder) as vanilla:
        with vanilla.working_dir(build_directory):
            out, err = vanilla.exec(['./bin/foobar'])
            assert 'Current local time and date' in out, f"out: '{out}' err: '{err}'"

            out, err = vanilla.exec(['./bin/foobar_c'])
            assert 'Current date' in out, f"out: '{out}' err: '{err}'"
