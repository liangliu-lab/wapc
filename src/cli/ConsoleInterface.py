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

Console Interface class has been implemented to gather commands,
retrieve options and details and connect to device execute commands.

@package cli
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

"""

import cmd
import socket
import sys
from src.controller.main import Main
from time import gmtime, strftime
from src.helpers.Utils import Utils
from src.resources.Resources import Resources


class ConsoleInterface(cmd.Cmd):
    """
    Command list to implement all required methods pre-defined

    ConsoleInterface has been inherited from cmd library to handle
    commandline interface with user interaction. This class gathers commands
    from user and declare them into individual methods written in project
    own classes.

    """

    def __init__(self):
        """
            Constructure of ConsoleInterface class
        """
        cmd.Cmd.__init__(self)
        self.prompt = Resources.prompt

        #current timestamp
        self.now = strftime(Resources.time_format, gmtime())

        # main class instance to handle  gathered command
        self.main = Main()
        self.utils = Utils()

    def do_add(self, args):
        """
        add command insert a new device with its suddenly created configuration
        into inventory.

        Add methods push a default configuration by updating only IP value in
        configuration file with given IP and it insert a database record if
        device response is successfull with status code 110.

        @param args [-t] [--type] Add device, group, vlan, config
                [-i] [--ip] Use this params when adding some new variables
                which needs an ip such as device, config, etc.
                [-n] [--name] To set a name to related type variable
                [-u] [--username] Provide a username which will be used
                to connect device
        """

        try:
            self.main.add(args)
        except BaseException as exception:
            self.utils.logger.create_log(
                name="ConsoleInterface Exception",
                severity=self.utils.logger.severity.ERROR,
                line=self.utils.get_line(),
                message=str(exception.message),
                method="add [args]",
                facility="ConsoleInterface.do_add",
                host=socket.gethostname()
            )

    def do_edit(self, args):
        """
        edit command updates keys given with provided parameters in database.

        Edit method updates only database records by not touching recent device
        configuration. It is supposed that this operation is a soft update.

        @see Main.edit
        @param args [-t],[--type] Type of device, group, vlan, config, group
            [-o],[--option] Provide option to be updated in database
            [-P],[--parameter] Provide parameter to be set as a value
        """
        try:
            self.main.edit(args)
        except BaseException as exception:
            self.utils.logger.create_log(
                name="ConsoleInterface Exception",
                severity=self.utils.logger.severity.ERROR,
                line=self.utils.get_line(),
                message=str(exception.message),
                method="do_edit",
                facility="ConsoleInterface.do_up",
                host=socket.gethostname()
            )

    def do_group(self, args):
        """
        group command groups provided devices into given group one by one.

        Group devices with given parameters.

        @see Main().group()
        @param args  [-t] [--type] Type of device or group
                     [-g],[--group] Group id if you want to insert into group
                     [-i],[--id] Define id of device
        """
        try:
            self.main.group(args)
        except BaseException as exception:
            self.utils.logger.create_log(
                name="ConsoleInterface Exception",
                severity=self.utils.logger.severity.ERROR,
                line=self.utils.get_line(),
                message=str(exception.message),
                method="do_group",
                facility="ConsoleInterface.do_group",
                host=socket.gethostname()
            )

    def do_set(self, args):
        """
        set command set device recent configuration to given values
        value and update recent records in database by provided type

        Unset device or group with given parameters

        @see Main().set()
        @param args  [-t] [--type] Type of device or group
                     [-o],[--option] Provide option must be one of
                     [-i],[--id] Define id of device or group
        """
        try:
            self.main.set(args)
        except BaseException as exception:
            self.utils.logger.create_log(
                name="ConsoleInterface Exception",
                severity=self.utils.logger.severity.ERROR,
                line=self.utils.get_line(),
                message=str(exception.message),
                method="do_set",
                facility="ConsoleInterface.do_set",
                host=socket.gethostname()
            )

    def do_unset(self, args):
        """
        unset command unset device recent configuration to a default or none
        value and update recent records in database by provided type

        Unset device or group with given parameters

        @see Main().unset()
        @param args  [-t] [--type] Type of device or group
                     [-o],[--option] Provide option must be one of
                     [-i],[--id] Define id of device or group
        """
        try:
            self.main.unset(args)
        except BaseException as exception:
            self.utils.logger.create_log(
                name="ConsoleInterface Exception",
                severity=self.utils.logger.severity.ERROR,
                line=self.utils.get_line(),
                message=str(exception.message),
                method="do_unset",
                facility="ConsoleInterface.do_unset",
                host=socket.gethostname()
            )

    def do_ls(self, args):
        """
        ls command implements a list method to get
        recent records from database by provided type

        Show device, group, vlan, config etc with given parameters

        @see Main().list()
        @param args  [-t] [--type] Type of device or group
                     [-g],[--group] Group id if you want to list from group
                     [-i],[--id] Define id of device or group
        """
        try:
            self.main.list(args)
        except BaseException as exception:
            self.utils.logger.create_log(
                name="ConsoleInterface Exception",
                severity=self.utils.logger.severity.ERROR,
                line=self.utils.get_line(),
                message=str(exception.message),
                method="do_ls",
                facility="ConsoleInterface.do_ls",
                host=socket.gethostname()
            )

    def do_sh(self, args):
        """
        sh command implements a show method to get
        recent device config options

        Show device or group with given parameters
        Options can be one of: ssid, channel, ip, cpu, memory, channel, conf,
        firmware, model, serial, clients, run or any "show_" commands provided
        in wapc_condif.json

        @see Main().show()
        @param args [-t],[--type] Type of device or group
                    [-o],[--option] Provide option must be one of
                    [-i],[--id] Define id of device or group
        """
        try:
            self.main.show(args)
        except BaseException as exception:
            self.utils.logger.create_log(
                name="ConsoleInterface Exception",
                severity=self.utils.logger.severity.ERROR,
                line=self.utils.get_line(),
                message=str(exception.message),
                method="do_sh",
                facility="ConsoleInterface.do_sh",
                host=socket.gethostname()
            )

    def do_rm(self, args):
        """
        rm command removes given device, config or group from database

        Remove command removes given type from only database and the recent
        configuration on the device will still remains as it is. It is should be
        added again and then the default configuration file will be pushed into
        device again.

        @see Main().show()
        @param args [-t],[--type] Type of device or group
                    [-o],[--option] Provide option must be one of
                    [-i],[--id] Define id of device or group
        """
        try:
            self.main.remove(args)
        except BaseException as exception:
            self.utils.logger.create_log(
                name="ConsoleInterface Exception",
                severity=self.utils.logger.severity.ERROR,
                line=self.utils.get_line(),
                message=str(exception.message),
                method="do_rm",
                facility="ConsoleInterface.do_rm",
                host=socket.gethostname()
            )

    def do_selftest(self, args):
        """
        This method will implement a self testing
        with pre-defined parameters and values

        @param args
        """
        try:
            self.main.selftest(args)
        except BaseException as exception:
            self.utils.logger.create_log(
                name="ConsoleInterface Exception",
                severity=self.utils.logger.severity.ERROR,
                line=self.utils.get_line(),
                message=str(exception.message),
                method="do_selftest",
                facility="ConsoleInterface.do_selftest",
                host=socket.gethostname()
            )

    def do_help(self, args):
        """
        Prints help message

        @return help Detailed help message
        @param args
        """
        try:
            self.main.help(args)
        except BaseException as exception:
            self.utils.logger.create_log(
                name="ConsoleInterface Exception",
                severity=self.utils.logger.severity.ERROR,
                line=self.utils.get_line(),
                message=str(exception.message),
                method="do_help",
                facility="ConsoleInterface.do_help",
                host=socket.gethostname()
            )

    def cmdloop_with_keyboard_interrupt(self):
        """
        Keyboard interruption method

        """
        do_quit = False
        while not do_quit:
            try:
                self.cmdloop()
                do_quit = True
            except KeyboardInterrupt:
                sys.stdout.write('\n')
            # enable this when production
            except BaseException:
                sys.stdout.write('\n')

    def do_EOF(self, args):
        """
        @param args
        @return Exits from application
        """
        return True