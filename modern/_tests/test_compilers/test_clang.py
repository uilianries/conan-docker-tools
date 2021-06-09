import pytest


@pytest.mark.compiler('clang')
@pytest.mark.service('builder', 'deploy')
class TestClangCompiler:

    def test_version(self, container):
        out, err = container.exec(['clang', '--version'])
        assert err == 'all'

