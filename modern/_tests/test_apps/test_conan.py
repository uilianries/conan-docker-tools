from fixtures.expected import Expected


def test_conan_version(container, expected: Expected):
    output, _ = container.exec(['conan', '--version'])
    assert output.rstrip() == f'Conan version {expected.conan}'


def test_default_profile(container):
    pass


def test_python_version(container):
    pass
