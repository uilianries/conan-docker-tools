import pytest
from fixtures.expected import Version

IMAGL_REF = 'imagl/0.2.1@'


@pytest.mark.compiler('clang')
@pytest.mark.service('deploy')
def test_imagl_clang(container, expected):
    # imaGL library requires C++20 to build
    if expected.compiler.version.lazy_lt_semver(Version("10")):
        pytest.skip('Requires C++20 (clang >= 10')

    # Compile the project
    with container.working_dir():
        container.exec(['conan', 'install', IMAGL_REF, '--build', '-o', 'imagl:shared=True'])
        container.exec(['conan', 'install', IMAGL_REF, '-g', 'deploy', '-o', 'imagl:shared=True'])
        out, err = container.exec(['ldd', 'imagl/lib/libimaGL.so'])
        assert 'libc++.so.1 => /usr/local/lib/libc++.so.1' in out


@pytest.mark.compiler('gcc')
@pytest.mark.service('deploy')
@pytest.mark.parametrize("libcxx", ['libstdc++', 'libstdc++11'])
def test_imagl_gcc(container, expected, libcxx):
    if expected.compiler.version.lazy_lt_semver(Version("9")):
        pytest.skip('Requires C++20 (gcc >= 9')

    # Compile the project
    with container.working_dir():
        container.exec(['conan', 'install', IMAGL_REF, '--build', '-s', f'compiler.libcxx={libcxx}', '-o', 'imagl:shared=True'])
        container.exec(['conan', 'install', IMAGL_REF, '-g', 'deploy', '-s', f'compiler.libcxx={libcxx}', '-o', 'imagl:shared=True'])
        out, err = container.exec(['ldd', 'imagl/lib/libimaGL.so'])
        assert 'libstdc++.so.6 => /usr/local/lib64/libstdc++.so.6' in out
        assert 'libgcc_s.so.1 => /usr/local/lib64/libgcc_s.so' in out
