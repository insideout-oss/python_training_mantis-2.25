import ftplib
import json
import os.path
import platform

import pytest
import importlib
import ftputil

from fixture.application import Application

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture
def app(request, config):
    global fixture
    webadmin = config['webadmin']
    browser = request.config.getoption("--browser")
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    fixture.session.ensure_login(username=webadmin['username'], password=webadmin['password'])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)


QUICK_FTP_PORT = 8021


class MySession(ftplib.FTP):
    def __init__(self, host, userid, password, port):
        """Act like ftplib.FTP's constructor but connect to another port."""
        ftplib.FTP.__init__(self)
        self.connect(host, port)
        self.login(userid, password)


def install_server_configuration(host, username, password):
    # access denied error on Mac (exception raised on file renaming)
    if platform.system() == "Windows":
        with ftputil.FTPHost(host, username, password, port=QUICK_FTP_PORT, session_factory=MySession) as remote:
            if remote.path.isfile("config/config_inc.php.bak"):
                remote.remove("config/config_inc.php.bak")
            if remote.path.isfile("config/config_inc.php"):
                remote.rename("config/config_inc.php", "config/config_inc.php.bak")
            fromfile = os.path.join(os.path.dirname(__file__), "resources/config_inc.php")
            remote.upload(fromfile, "config/config_inc.php.bak")


def restore_server_configuration(host, username, password):
    # access denied error on Mac (exception raised on file renaming)
    if platform.system() == "Windows":
        with ftputil.FTPHost(host, username, password, port=QUICK_FTP_PORT, session_factory=MySession) as remote:
            if remote.path.isfile("config/config_inc.php.bak"):
                if remote.path.isfile("config/config_inc.php"):
                    remote.remove("config/config_inc.php")
                remote.rename("config/config_inc.php.bak", "config/config_inc.php")


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        if fixture.session is not None:
            fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")


def pytest_generate_tests(metafunc):
    for f in metafunc.fixturenames:
        if f.startswith("data_"):
            testdata = load_from_module(f[5:])
            metafunc.parametrize(f, testdata, ids=[str(x) for x in testdata])


def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata
