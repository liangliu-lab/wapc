#!/opt/python/bin/python
# coding=utf-8
"""
Copyright 2013 Labris Technology.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@package bin
@date 4/25/13
@author 'fatih'
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Teknoloji

"""
import sys
import os
PARENTDIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, '%s' % PARENTDIR)

import socket
from src.helpers.Utils import Utils
from src.model.Log import Log
from src.resources.Resources import Resources
from src.controller.Logger import Logger
from src.controller.DeviceMethods import DeviceMethods
from argparse import Namespace
import time
import atexit
from signal import SIGTERM


class Daemon:
    """
        A generic daemon class.

        Usage: subclass the Daemon class and override the run() method
        """

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null',
                 stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.daemon_commands = Resources.daemon_commands
        self.utils = Utils()
        self.logger = Logger(self.utils.daemon_prefix %
                             {'time': self.utils.day})
        self.log = Log()

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write(
                "fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write(
                "fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        try:
            # redirect standard file descriptors
            sys.stdout.flush()
            sys.stderr.flush()
            si = file(self.stdin, 'r')
            so = file(self.stdout, 'a+')
            se = file(self.stderr, 'a+', 0)
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

            # write pidfile
            atexit.register(self.delpid)
            pid = str(os.getpid())
            os.seteuid(0)
            file(self.pidfile, 'w+').write("%s\n" % pid)
        except BaseException as exception:
            print exception.message

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
                Start the daemon
                """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError as error:
            pid = None
            print error.message

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
                Stop the daemon
                """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        """
                Restart the daemon
                """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon.
        It will be called after the process has been
        demonized by start() or restart().
        """
        args = Namespace
        self.device_methods = DeviceMethods(args)
        device_list = self.device_methods.get_device_list()

        while True:
            try:
                for device in device_list:
                    args.id = str(device[0])
                    device_name = str(device[1])
                    host = str(device[3])
                    for command in self.daemon_commands:
                        args.option = command
                        response = self.device_methods.show(args)
                        self.logger.create_log(
                            name="Log for %(name)s" % {'name': device_name},
                            severity=self.log.severity.INFO,
                            line=self.utils.get_line(),
                            message=response,
                            method="Daemon.run",
                            facility=command,
                            host=host
                        )
            except BaseException as exception:
                self.logger.create_log(
                    name="Daemon Exception",
                    severity=self.logger.severity.FATAL,
                    line=self.utils.get_line(),
                    message=str(exception.message),
                    method="run",
                    facility="Daemon.run",
                    host=socket.gethostname()
                )
            time.sleep(self.utils.daemon_timeout)

if __name__ == "__main__":
    try:
        my_daemon = Daemon('/var/run/wapc.pid')
        #sys.argv.append('start')
        if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                    my_daemon.start()
            elif 'stop' == sys.argv[1]:
                    my_daemon.stop()
            elif 'restart' == sys.argv[1]:
                    my_daemon.restart()
            else:
                    print "Unknown command"
                    sys.exit(2)
            sys.exit(0)
        else:
            print "usage: %s start|stop|restart" % sys.argv[0]
            sys.exit(2)
    except BaseException as exception:
        my_daemon.logger.create_log(
            name="Daemon Exception",
            severity=my_daemon.logger.severity.FATAL,
            line=my_daemon.utils.get_line(),
            message=str(exception.message),
            method="run",
            facility="Daemon.run",
            host=socket.gethostname()
        )
