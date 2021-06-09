import pytest


@pytest.mark.compiler('gcc')
@pytest.mark.service('builder', 'deploy')
class TestGccCompiler:

    def test_version(self, container):
        out, _ = container.exec(['gcc', '--version'])
        assert out == 'all'

