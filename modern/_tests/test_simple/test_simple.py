import pytest
from fixtures.container import run_container
import os
"""
#!/bin/bash

set -ex

mkdir -p /tmp/build/simple
rm -rf /tmp/build/simple/*

pushd /tmp/build/simple

cmake /tmp/workingdir/simple -DCMAKE_BUILD_TYPE=Release
cmake --build .

./example-c
./example-cpp
"""

@pytest.mark.service('deploy')
def test_simple(container, expected):
    build_directory = '/tmp/build/simple'
    # Compile the project
    container.exec(['mkdir', 'simple'], working_dir='/tmp/build')
    container.exec(['cmake', '/tmp/workingdir/simple', '-DCMAKE_BUILD_TYPE=Release'], working_dir=build_directory)
    container.exec(['cmake', '--build', '.'], working_dir=build_directory)

    out, err = container.exec(['./example-c'], working_dir=build_directory)
    assert 'Current local time and date' in out, f"out: '{out}' err: '{err}'"
    out, err = container.exec(['./example-cpp'], working_dir=build_directory)
    assert 'Current date' in out, f"out: '{out}' err: '{err}'"

    # Check we can run these executables in vanilla image
    vanilla_img = f"{expected.distro.name}:{expected.distro.version}"
    with run_container(vanilla_img, tmpdirname=container._tmpfolder) as vanilla:
        out, _ = vanilla.exec(['./example-c'], working_dir=build_directory)
        assert 'Current local time and date' in out, f"out: '{out}' err: '{err}'"

        out, err = vanilla.exec(['./example-cpp'], working_dir=build_directory)
        assert 'Current date' in out, f"out: '{out}' err: '{err}'"
