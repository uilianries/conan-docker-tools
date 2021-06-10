# Tests for Python

def test_python_version(container, expected):
    output, _ = container.exec(['python', '--version'])
    assert output.rstrip() == f'Python {expected.python}'
