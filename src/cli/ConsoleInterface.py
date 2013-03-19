# coding=utf-8
"""
    Console Interface class has been implemented to gather commands, retrieve options and details and connect to device
    execute commands.
"""

import cmd
import sys
from src.controller.main import Main
from time import gmtime, strftime
from src.resources.resources import Resources


class ConsoleInterface(cmd.Cmd):
    """
        Command list to implement all required methods
    """
    cmd.Cmd.prompt = Resources.prompt
    now = strftime(Resources.time_format, gmtime())
    main = Main()

    def do_add(self, args):
        """
        Add device, group, vlan, config etc with given parameters
                [-t] [--type] Add device, group, vlan, config
                [-i] [--ip] Use this params when adding some new variables which needs an ip such as device, config, etc.
                [-n] [--name] To set a name to related type variable
                [-u] [--username] Provide a username which will be used to connect device
            :param args:
            """
        try:
            self.main.add(args)
        except Exception as e:
            print e.message
            pass

    def do_edit(self, args):
        """
        Edit details of given type of device with given parameters
            [-t] [--type] Add device, group, vlan, config, group
            [-i] [--ip] Use this params when adding some new variables which needs an ip such as device, config, etc.
            [-n] [--name] To set a name to related type variable
            [-u] [--username] Provide a username which will be used to connect device
        :param args:
        """
        try:
            self.main.edit(args)
        except Exception as e:
            print e.message
            pass

    def do_group(self, args):
        """
                Add new group with params
        :param args:
        """
        try:
            self.main.group(args)
        except Exception as e:
            print e.message
            pass

    def do_set(self, args):
        """
            Set options with given values to a device or group with params
        :param args:
        """
        try:
            self.main.set(args)
        except Exception as e:
            print e.message
            pass

    def do_unset(self, args):
        """
            Set options with given values to a device or group with params
        :param args:
        """
        try:
            self.main.unset(args)
        except Exception as e:
            print e.message
            pass

    def do_ls(self, args):
        """
            List all details of any type given
        :param args:
        """
        try:
            self.main.list(args)
        except Exception as e:
            print e.message
            pass

    def do_sh(self, args):
        """
        Add device, group, vlan, config etc with given parameters
                [-t] [--type] Add device, group, vlan, config
                [-o],[--option]\tProvide option must be one of
                [-i],[--id]\tDefine id of device or group
            :param args:
            """
        try:
            self.main.show(args)
        except Exception as e:
            print e.message
            pass

    def do_rm(self, args):
        """
            Remove any given variable
        :param args:
            """
        try:
            self.main.remove(args)
        except Exception as e:
            print e.message
            pass

    def do_selftest(self, command):
        """
            This method will implement a self testing with pre-defined parameters and values
        :param command:
            """

    def do_help(self, args):
        """
        :rtype : object
        :param args:
        """
        try:
            self.main.help(args)
        except Exception as e:
            print e.message
            pass

    def do_exit(self, args):
        """
            Exit command
        :rtype : object
            :param args:
        """
        try:
            sys.exit(0)
        except Exception as e:
            print e.message
            pass

    def preloop(self):
        """
            Preloop is a helper method to handle commands before loop executed

        """
        cmd.Cmd.preloop(self)
        self._hist = []
        self._locals = {}
        self._globals = {}

    def postloop(self):
        """
            Postloop is a helper method to declare command will be run after loop executed

        """
        cmd.Cmd.postloop(self)
        print "Exiting ..."

    def precmd(self, line):
        """

        :param line:
        :return:
        """
        self._hist += [ line.strip() ]
        return line

    def postcmd(self, stop, line):
        """

        :param stop:
        :param line:
        :return:
        """
        return stop

    def emptyline(self):
        """


        :return:
        """
        return cmd.Cmd.emptyline(self)

    def cmdloop_with_keyboard_interrupt(self):
        """
            Keyboard interruption method

        """
        doQuit = False
        while not doQuit:
            try:
                self.cmdloop()
                doQuit = True
            except KeyboardInterrupt:
                sys.stdout.write('\n')
            # enable this when production
            except BaseException:
                sys.stdout.write('\n')


    def do_EOF(self, args):
        """

        :param args:
        :return:
        """
        return self.do_exit(args)
