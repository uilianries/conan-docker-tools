import os.path
import re
from dataclasses import dataclass

import pytest
import yaml


@dataclass
class Version:
    full_version: str = None
    major: str = None
    minor: str = None
    patch: str = None

    def __init__(self, full_version=None):
        if not full_version:
            return

        self.full_version = full_version
        self.major, *rest = self.full_version.split('.', 1)
        if rest:
            self.minor, *rest = rest[0].split('.', 1)
            if rest:
                self.patch = rest[0]

    def __str__(self):
        ret = f"{self.major}"
        if self.minor:
            ret += f".{self.minor}"
        if self.patch:
            ret += f".{self.patch}"
        return ret


@dataclass
class Distro:
    name: str
    version: Version


@dataclass
class Compiler:
    name: str
    version: Version


@dataclass
class Expected:
    distro: Distro
    python: Version
    cmake: Version
    conan: Version = None
    compiler: Compiler = None


def get_compiler_version(compiler_name, compiler_major):
    docker_file = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'docker-compose.yml'))
    with open(docker_file, 'r') as f:
        data = yaml.safe_load(f)

    if compiler_name == 'gcc':
        return data.get(f'x-gcc{compiler_major}').get('GCC_VERSION')
    elif compiler_name == 'clang':
        return data.get(f'x-llvm{compiler_major}').get('LLVM_VERSION')
    else:
        raise NotImplemented


@pytest.fixture(scope="session")
def expected(request) -> Expected:
    # Parse the image filename
    image = request.config.option.image
    m = re.match(r'((?P<domain>[\w.]+)\/)?'
                 r'(?P<username>[\w.]+)\/'
                 r'((?P<compiler>gcc|clang)(?P<version>\d+)-)?'
                 r'((?P<service>base|builder|deploy|conan)-)?'
                 r'(?P<distro>[a-z]+)(?P<distro_version>[\d.]+)'
                 r'(-(?P<jenkins>jenkins))?'
                 r'(:(?P<conan>[\d.]+))?', image)

    # Parse the envfile used to generate the docker images
    envfile = request.config.option.env_file
    env_values = {}
    with open(envfile, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                print(line)
                key, value = line.split('=')
                env_values[key] = value

    distro = Distro(m.group('distro'), Version(m.group('distro_version')))
    python = Version(env_values.get('PYTHON_VERSION'))
    cmake = Version(env_values.get('CMAKE_VERSION_FULL'))
    expected = Expected(distro, python, cmake)

    if m.group('conan'):
        expected.conan = Version(m.group('conan'))
        assert str(expected.conan) == env_values.get('CONAN_VERSION')

    if m.group('compiler'):
        compiler = m.group('compiler')
        major = m.group('version')
        full_version = get_compiler_version(compiler, major)
        expected.compiler = Compiler(compiler, Version(full_version))

    return expected


@pytest.fixture(autouse=True)
def skip_by_compiler(request, expected):
    if request.node.get_closest_marker('compiler'):
        if request.node.get_closest_marker('compiler').args[0] != expected.compiler.name:
            pytest.skip('skipped for this compiler: {}'.format(expected.compiler.name))