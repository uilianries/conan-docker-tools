import pytest
from fixtures.expected import Expected


@pytest.mark.compiler('gcc')
@pytest.mark.service('builder', 'deploy')
class TestGccCompiler:

    def test_version(self, container, expected: Expected):
        out, _ = container.exec(['gcc', '--version'])
        assert out == expected.compiler.version

