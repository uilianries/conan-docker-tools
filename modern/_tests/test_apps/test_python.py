
# Tests for Python

def test_python_version(container):
    output, _ = container.exec(['python', '--version'])
    assert output.rstrip() == 'Python 3.6'  # Forced by Conan tribe.


# TODO: x86 version?
