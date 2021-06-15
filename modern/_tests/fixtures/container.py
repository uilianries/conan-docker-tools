import os
import subprocess
import tempfile
import uuid
from contextlib import contextmanager

import pytest


class DockerContainer:
    def __init__(self, image, tmpfolder=None):
        self.image = image
        self.name = str(uuid.uuid4())
        self._tmpfolder = tmpfolder
        self.tmp = '/tmp/build'
        self._working_dir = None

    def run(self):
        mount_volume = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'workingdir'))
        args = ["docker", "run", "-t", "-d", "-v", f"{mount_volume}:/tmp/workingdir"]
        if self._tmpfolder:
            args += ["-v", f"{self._tmpfolder}:{self.tmp}"]
        args += ["--name", self.name, self.image]
        subprocess.check_call(args)

    @contextmanager
    def working_dir(self, working_dir=None):
        wdir = working_dir or os.path.join('/tmp', str(uuid.uuid4()))
        try:
            self.exec(['mkdir', '-p', wdir])
            self._working_dir = wdir
            yield
        finally:
            self._working_dir = None

    def bash(self, bash_commands: list):
        return self.exec(['/bin/bash', ] + bash_commands)

    def exec(self, commands: list):
        args = ["docker", "exec"]
        if self._working_dir:
            args += ["-w", self._working_dir]
        args += [self.name, ] + commands
        print(f'>> {" ".join(args)}')
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout.decode('utf-8'), stderr.decode('utf-8')

    def stop(self):
        subprocess.check_call(["docker", "stop", self.name])
        subprocess.check_call(["docker", "rm", "-f", self.name])


@contextmanager
def run_container(image, tmpdirname):
    container = DockerContainer(image, tmpdirname)
    try:
        container.run()
        yield container
    finally:
        container.stop()


@pytest.fixture(scope="session")
def container(pytestconfig):
    image = pytestconfig.getoption("image")
    with tempfile.TemporaryDirectory() as tmpdirname:
        with run_container(image, tmpdirname) as container:
            yield container
