# coding=utf-8
import cmd
from src.functions.main import Main
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
                [-t] [--type] Add device, group, vlan, config, group
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

    def do_vlan(self, args):
        """
                Add new vlan with params
        :param args:
            """
        try:
            self.main.vlan(args)
        except Exception as e:
            print e.message

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
                Show command
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

    def do_config(self, args):
        """
                Create new config for devices
            :param args:
            """
        try:
            self.main.configure(args)
        except Exception as e:
            print e.message
            pass

    def do_selftest(self, command):
        """

            """

    def do_help(self, args):
        """
                Show help
        :param args:
            """
        try:
            self.main.help(args)
        except Exception as e:
            print e.message
            pass

    def do_EOF(self, line):
        """

        :param line:
        :return:
        """
        return True
