import os
import time
from subprocess import Popen
from typing import List

from flask import Flask

TOR_PATH = '/Applications/Tor Browser.app/Contents/MacOS/Tor/tor.real'


def open_tor_process(tor_path, port):
    from tempfile import mkstemp
    fd, tmp = mkstemp(".torrc")
    fd_datadir, data_dir = mkstemp(".data")
    os.unlink(data_dir)
    os.makedirs(data_dir)

    with open(tmp, "w") as f:
        f.write("SOCKSPort {}\n".format(port))
        f.write("DataDirectory {}\n".format(data_dir))

    process = Popen([tor_path, "-f", tmp], cwd=os.path.dirname(data_dir))
    return process


class Tor:

    def __init__(self, tor_path: str, port: int):
        self.tor_path = tor_path
        self.port = port
        self.popen = self.open_tor_process(port)
        self.count = 0

    def is_terminated(self):
        return self.popen.poll() is not None

    def open_tor_process(self, port):
        from tempfile import mkstemp
        fd, tmp = mkstemp(".torrc")
        fd_datadir, data_dir = mkstemp(".data")
        os.unlink(data_dir)
        os.makedirs(data_dir)

        with open(tmp, "w") as f:
            f.write("SOCKSPort {}\n".format(port))
            f.write("DataDirectory {}\n".format(data_dir))

        return Popen([self.tor_path, "-f", tmp], cwd=os.path.dirname(data_dir))

    def incr_used_count(self):
        self.count = self.count + 1


class TorManager:

    def __init__(self, tor_path: str, num_of_instances=3):
        self.tor_path = tor_path
        self.num_of_instances = num_of_instances
        self.tor_instances: List[Tor] = []
        self.next_port = 9950

        for x in range(num_of_instances):
            self.create_tor()

    def create_tor(self):
        self.next_port = self.next_port + 1
        self.tor_instances.append(Tor(self.tor_path, self.next_port))

    def maintain(self):
        dead_list = []
        for tor in self.tor_instances:
            if tor.is_terminated():
                dead_list.append(tor)
                continue
            if tor.count >= 5:
                try:
                    tor.popen.terminate()
                except BaseException:
                    pass
                dead_list.append(tor)

        for d in dead_list:
            self.tor_instances.remove(d)

        while len(self.tor_instances) < self.num_of_instances:
            self.create_tor()

    def remove_by_port(self, port):
        selected = [x for x in self.tor_instances if x.port == port]
        for tor in selected:
            try:
                tor.popen.terminate()
            except BaseException:
                pass
            self.tor_instances.remove(tor)
        pass


dispatch_count = 0


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        print(app.instance_path)
        os.makedirs(app.instance_path)
    except OSError:
        pass

    tor_manager = TorManager(tor_path=TOR_PATH)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        global dispatch_count
        tor_manager.maintain()
        dispatch_count = dispatch_count + 1
        index = dispatch_count % len(tor_manager.tor_instances)
        selected = tor_manager.tor_instances[index]
        selected.incr_used_count()

        return {"port": selected.port, "used_count": selected.count}

    @app.route('/remove/<port>')
    def remove(port: int):
        tor_manager.remove_by_port(port)
        return "ok"

    return app
