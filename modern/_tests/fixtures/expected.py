import pytest
from dataclasses import dataclass

@dataclass
class Version:
    major: str
    minor: str
    patch: int = None

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass
class Distro:
    name: str
    version: Version


@dataclass
class Compiler:
    name: str
    version: int

@dataclass
class Expected:
    distro: Distro
    python: Version
    conan: Version
    cmake: Version
    compiler: Compiler


@pytest.fixture(scope="session")
def expected(request) -> Expected:
    image = request.config.option.image

    # TODO: Improve parsing
    distro = Distro('ubuntu', Version('16', '04'))

    compiler_name = 'gcc' if 'gcc' in image else 'clang'
    compiler_version = '11'
    compiler = Compiler(compiler_name, compiler_version)

    python = Version('3', '8', '8')
    conan = Version('1', '37', '1')
    cmake = Version('3', '20', '2')

    return Expected(distro, python, conan, cmake, compiler)


@pytest.fixture(autouse=True)
def skip_by_compiler(request, expected):
    if request.node.get_closest_marker('compiler'):
        if request.node.get_closest_marker('compiler').args[0] != expected.compiler.name:
            pytest.skip('skipped for this compiler: {}'.format(expected.compiler.name)) 
