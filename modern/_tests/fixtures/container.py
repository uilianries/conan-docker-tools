import pytest
import subprocess
import uuid
import os


class DockerContainer:
    def __init__(self, image):
        self.image = image
        self.name = str(uuid.uuid4())
    
    def run(self):
        mount_volume = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        subprocess.check_call(["docker", "run", "-t", "-d", "-v", f"{mount_volume}:/tmp/project", "--name", self.name, self.image])
    
    def exec(self, bash_commands: list):
        args = ["docker", "exec", self.name, "/bin/bash"] + bash_commands
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout.decode('utf-8'), stderr.decode('utf-8')

    def stop(self):
        subprocess.check_call(["docker", "stop", self.name])
        subprocess.check_call(["docker", "rm", "-f", self.name])



@pytest.fixture(scope="session")
def container(pytestconfig):
    image = pytestconfig.getoption("image")
    container = DockerContainer(image)
    try:
        container.run()
        yield container
    finally:
        container.stop()
