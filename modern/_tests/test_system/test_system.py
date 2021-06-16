import pytest


@pytest.mark.service('deploy')
def test_system(container, expected):
    with container.working_dir():
        container.exec(["conan", "config", "set", "general.sysrequires_mode=enabled"])
        container.exec(["sudo", "cp", "/tmp/workingdir/system/sources.list", "/etc/apt/sources.list"])
        container.exec(["sudo", "apt-key", "adv", "--keyserver", "keyserver.ubuntu.com", "--recv-keys", "60C317803A41BA51845E371A1E9377A2BA9EF27F"])
        container.exec(["sudo", "apt-get", "-qq", "update"])
        container.exec(
            ["sudo", "apt-get", "-qq", "install", "-y", "--force-yes", "--no-install-recommends", "--no-install-suggests", "-o=Dpkg::Use-Pty=0",
             "g++-9"])
        container.exec(["conan", "install", "/tmp/workingdir/system", "--build"])
        container.exec(["cmake", "/tmp/workingdir/system", "-DCMAKE_BUILD_TYPE=Release"])
        container.exec(["cmake", "--build", "."])

        out, err = container.exec(['ldd', 'bin/package_test'])
        assert 'libstdc++.so.6 => /usr/local/lib64/libstdc++.so.6' in out, f"out: '{out}' err: '{err}'"
        assert 'libgcc_s.so.1 => /usr/local/lib64/libgcc_s.so.1' in out, f"out: '{out}' err: '{err}'"
