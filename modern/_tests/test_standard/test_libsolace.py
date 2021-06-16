import pytest
from fixtures.expected import Version

LIBSOLACE_REF = 'libsolace/0.3.9@'


@pytest.mark.compiler('clang')
@pytest.mark.service('deploy')
@pytest.mark.parametrize("libcxx", ['libc++', 'libstdc++', 'libstdc++11'])
def test_libsolace_clang(container, expected, libcxx):
    # imaGL library requires C++20 to build
    if expected.compiler.version.lazy_lt_semver(Version("10")):
        pytest.skip('Requires C++20 (clang >= 10')

    # Compile the project
    with container.working_dir():
        container.exec(['conan', 'install', LIBSOLACE_REF, '--build', '-s', f'compiler.libcxx={libcxx}', '-o', 'imagl:shared=True'])
        container.exec(['conan', 'install', LIBSOLACE_REF, '-g', 'deploy', '-s', f'compiler.libcxx={libcxx}', '-o', 'imagl:shared=True'])
        out, err = container.exec(['ldd', 'libsolace/lib/libsolace.so'])
        assert 'libc++.so.1 => /usr/local/lib/libc++.so.1' in out, f"out: '{out}' err: '{err}'"


@pytest.mark.compiler('gcc')
@pytest.mark.service('deploy')
@pytest.mark.parametrize("libcxx", ['libstdc++', 'libstdc++11'])
def test_libsolace_gcc(container, expected, libcxx):
    if expected.compiler.version.lazy_lt_semver(Version("9")):
        pytest.skip('Requires C++20 (gcc >= 9')

    # Compile the project
    with container.working_dir():
        container.exec(['conan', 'install', LIBSOLACE_REF, '--build', '-s', f'compiler.libcxx={libcxx}', '-o', 'imagl:shared=True'])
        container.exec(['conan', 'install', LIBSOLACE_REF, '-g', 'deploy', '-s', f'compiler.libcxx={libcxx}', '-o', 'imagl:shared=True'])
        out, err = container.exec(['ldd', 'libsolace/lib/libsolace.so'])
        assert 'libstdc++.so.6 => /usr/local/lib64/libstdc++.so.6' in out, f"out: '{out}' err: '{err}'"
        assert 'libc.so.6 => /lib/x86_64-linux-gnu/libc.so' in out, f"out: '{out}' err: '{err}'"
