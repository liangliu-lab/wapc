import cmd
from src.cli.CommunicationInterface import CommunicationInterface
from src.cli.Utils import Utils
from src.functions.main import Main
from src.language.language import Language
from src.model.Device import Device
from src.model.Config import Config
from src.database.db import Database
from time import gmtime, strftime
from src.resources.resources import Resources


class ConsoleInterface(cmd.Cmd):
    """
        Command list to implement all required methods
    """
    cmd.Cmd.prompt = Resources.prompt
    config = Config()
    device = Device()
    ci = CommunicationInterface()
    db = Database()
    now = strftime(Resources.time_format, gmtime())
    script = Resources.ci_script
    cfg_device = Resources.cfg_device_resource
    main = Main()

    def do_add(self, args):
        """
            [-t] [--type] Add device, group, vlan, config, group
            [-i] [--ip] Use this params when adding some new variables which needs an ip such as device, config, etc.
            [-n] [--name] To set a name to related type variable
            [-u] [--username] Provide a username which will be used to connect device
        """
        try:
            self.main.add(args)
        except Exception as e:
            print e.message
            pass

    def do_group(self, args):
        """
            Add new group with params
        """
        try:
            self.main.group(args)
        except Exception as e:
            print e.message
            pass

    def do_vlan(self, args):
        """
            Add new vlan with params
        """
        try:
            self.main.group(args)
        except Exception as e:
            print e.message

    def do_ls(self, args):
        """
            List all details of any type given
        """
        try:
            self.main.list(args)
        except Exception as e:
            print e.message
            pass

    def do_sh(self, args):
        """
            Show command
        """
        try:
            self.main.show(args)
        except Exception as e:
            print e.message
            pass

    def do_rm(self, args):
        """
            Remove any given variable
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
        """
        try:
            self.main.help(args)
        except Exception as e:
            print e.message
            pass

    def do_EOF(self, line):
        return True
