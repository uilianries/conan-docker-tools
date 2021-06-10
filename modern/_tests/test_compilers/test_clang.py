import pytest


@pytest.mark.compiler('clang')
@pytest.mark.service('builder', 'deploy', 'conan')
class TestClangCompiler:

    def test_version(self, container, expected):
        out, err = container.exec(['clang', '--version'])
        assert expected.compiler.name == 'clang'
        assert err == expected.compiler

