#!/usr/bin/env python
import re
import sys
import os
import subprocess
import random
import logging


def get_conan_target_version():
    env_file = open(".env", "r")
    match = re.search("CONAN_VERSION=(.*)", env_file.read())
    if not match:
        return "latest"
    return match.group(1)


def get_libstdcpp_patch_version():
    env_file = open(".env", "r")
    match = re.search("LIBSTDCPP_PATCH_VERSION=(.*)", env_file.read())
    if not match:
        return "latest"
    return match.group(1)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO)
    compiler = sys.argv[1]
    container = compiler + "-" + str(random.randint(1, 9999))
    pwd = os.getcwd()
    libstdcpp_patch = get_libstdcpp_patch_version()
    image = "{}/{}-ubuntu16.04:{}".format(os.getenv("DOCKER_USERNAME", "conanio"), compiler, get_conan_target_version())
    exit_code = 0

    try:
        logging.info("Starting test: GCC (Internal)")
        subprocess.check_call(["docker", "run", "-t", "-d", "-v", "%s:/tmp/project" % pwd, "--name", container, image])
        subprocess.check_call(["docker", "exec", container, "/bin/bash", "/tmp/project/test/gcc/conan/test_conan.sh"])
        logging.info("Test result (GCC Internal): SUCCESS")
    except Exception as error:
        logging.error("Test result (GCC Internal): FAILURE - {}".format(error))
        exit_code = 1
    finally:
        subprocess.check_call(["docker", "stop", container])
        subprocess.check_call(["docker", "rm", "-f", container])

    if exit_code:
        sys.exit(exit_code)

    container = "ubuntu-" + str(random.randint(1, 9999))

    try:
        logging.info("Starting test: GCC (Vanilla)")
        subprocess.check_call(["docker", "run", "-t", "-d", "-v", "%s:/tmp/project" % pwd, "--name", container, "ubuntu:xenial"])

        subprocess.check_call(["docker", "exec", container, "cp", "/tmp/project/{}.tar".format(compiler), "/tmp/"])
        subprocess.check_call(["docker", "exec", container, "tar", "xf", "/tmp/{}.tar".format(compiler), "-C", "/tmp"])

        subprocess.check_call(["docker", "exec", container, "cp", "/tmp/bin/libstdc++.so.6.0.{}".format(libstdcpp_patch), "/usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.21"])
        subprocess.check_call(["docker", "exec", container, "/tmp/bin/foobar"])
        subprocess.check_call(["docker", "exec", container, "/tmp/bin/foobar_c"])
        logging.info("Test result (GCC Vanilla): SUCCESS")
    except Exception as error:
        logging.error("Test result (GCC Vanilla): FAILURE - {}".format(error))
        exit_code = 1
    finally:
        subprocess.check_call(["docker", "stop", container])
        subprocess.check_call(["docker", "rm", "-f", container])

    sys.exit(exit_code)
