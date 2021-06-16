import pytest
from fixtures.expected import Expected


@pytest.mark.compiler('gcc')
@pytest.mark.service('builder', 'deploy', 'conan')
class TestGccCompiler:

    def test_version(self, container, expected: Expected):
        out, _ = container.exec(['gfortran', '--version'])
        assert expected.compiler.name == 'gcc'
        first_line = out.splitlines()[0]
        assert first_line == f'GNU Fortran (GCC) {expected.compiler.version}'
