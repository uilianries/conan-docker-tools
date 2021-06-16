import pytest
from fixtures.container import run_container


@pytest.mark.compiler('clang')
@pytest.mark.service('deploy')
@pytest.mark.parametrize("libcxx", ['libc++', 'libstdc++', 'libstdc++11'])
def test_clang_conan(container, expected, libcxx):
    build_directory = '/tmp/build/clang_conan'
    # Compile the project
    with container.working_dir(build_directory):
        # TODO: Why debug?
        container.exec(
            ['conan', 'create', '/tmp/workingdir/clang_conan/conanfile.py', 'foo/0.1@user/testing', '--build', '-s', 'compiler.libcxx=libc++', '-s',
             'build_type=Debug'])
        container.exec(['conan', 'install', 'foo/0.1@user/testing', '-g', 'deploy', '-s', 'compiler.libcxx=libc++', '-s', 'build_type=Debug'])

        out, err = container.exec(['./bin/foobar'])
        assert 'Current local time and date' in out, f"out: '{out}' err: '{err}'"
        out, err = container.exec(['./bin/foobar_c'])
        assert 'Current date' in out, f"out: '{out}' err: '{err}'"

        out, err = container.exec(['ldd', 'bin/foobar'])
        if libcxx == 'libc++':
            assert 'libgcc' not in out, f"out: '{out}' err: '{err}'"
            assert 'libc++.so.1 => /usr/local/lib/libc++.so.1' in out, f"out: '{out}' err: '{err}'"
        else:
            assert 'libc++' not in out, f"out: '{out}' err: '{err}'"
            assert 'libc++abi' not in out, f"out: '{out}' err: '{err}'"
            assert 'libgcc_s.so.1 => /usr/local/lib64/libgcc_s.so.1' in out, f"out: '{out}' err: '{err}'"
            assert 'libstdc++.so.6 => /usr/local/lib64/libstdc++.so.6' in out, f"out: '{out}' err: '{err}'"
        assert 'libllvm-unwind.so.1 => /usr/local/lib/libllvm-unwind.so.1' in out, f"out: '{out}' err: '{err}'"

        out, err = container.exec(['ldd', 'bin/foobar_c'])
        if libcxx == 'libc++':
            assert 'libgcc' not in out, f"out: '{out}' err: '{err}'"
            assert 'libc++.so.1 => /usr/local/lib/libc++.so.1' in out, f"out: '{out}' err: '{err}'"
        else:
            assert 'libc++' not in out, f"out: '{out}' err: '{err}'"
            assert 'libc++abi' not in out, f"out: '{out}' err: '{err}'"
            assert 'libgcc_s.so.1 => /usr/local/lib64/libgcc_s.so.1' in out, f"out: '{out}' err: '{err}'"
            assert 'libstdc++.so.6 => /usr/local/lib64/libstdc++.so.6' in out, f"out: '{out}' err: '{err}'"
        assert 'libllvm-unwind.so.1 => /usr/local/lib/libllvm-unwind.so.1' in out, f"out: '{out}' err: '{err}'"

    # Check we can run these executables in vanilla image
    vanilla_img = f"{expected.distro.name}:{expected.distro.version}"
    with run_container(vanilla_img, tmpdirname=container._tmpfolder) as vanilla:
        with vanilla.working_dir(build_directory):
            out, err = vanilla.exec(['./bin/foobar'])
            assert 'Current local time and date' in out, f"out: '{out}' err: '{err}'"

            out, err = vanilla.exec(['./bin/foobar_c'])
            assert 'Current date' in out, f"out: '{out}' err: '{err}'"
