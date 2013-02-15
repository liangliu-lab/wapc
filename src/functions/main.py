# coding=utf-8

"""
    Documentation
    :author Fatih Karatana
"""

from Queue import Empty
from time import strftime, gmtime
import parser
from src.cli.ArgParser import ArgParser
from src.config.__sql__ import SQL
from src.database.db import Database
from src.helper.Utils import Utils
from src.language.language import Language
from src.resources.resources import Resources
from src.functions.DeviceMethods import DeviceMethods
from src.functions.GroupMethods import GroupMethods
from src.functions.ConfigMethods import ConfigMethods

__author__ = 'fatih'


class Main(dict):
    """
        Main class includes all base functions of the software
    """
    def __init__(self):
        self.deviceMethods = DeviceMethods()
        self.config = ConfigMethods()
        self.groups = GroupMethods()
        self.utils = Utils()
        self.argparser = ArgParser()
        self.now = strftime(Resources.time_format, gmtime())
        self.db = Database()

    def add(self, args):
        """


        :param args:
        """
        params = self.argparser.get_args(args)
        try:
            if params:
                # noinspection PyArgumentList
                if params.type == 'device':
                    # noinspection PyArgumentList
                    self.deviceMethods.create(params)
                elif params.type == 'group':
                    # noinspection PyArgumentList
                    GroupMethods.create(params)
                elif params.type == 'config':
                    # noinspection PyArgumentList
                    ConfigMethods.create(params)
                else:
                    print Language.MSG_ERR_GENERIC.format('91', 'No [type] argument provided')
            else:
                raise Exception("Something wrong with type")
                pass
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    def list(self, args):
        """
            list devices from inventory given
        :param args:
        """
        cmd = None
        flag = False

        try:
            params = self.argparser.get_args(args)
            #check namespace variables if set
            type = params.type
            #moderate type value to determine the statement
            if type == 'group':
                cmd = SQL.SQL_SELECT_GROUP_ALL
                flag = True
            elif type == 'device':
                cmd = SQL.SQL_SELECT_DEVICE_ALL
                flag = True
            elif type == 'config':
                cmd = SQL.SQL_SELECT_CONFIG
                flag = True
            elif type == 'vlan':
                cmd = SQL.SQL_SELECT_VLAN
                flag = True
            else:
                print Language.MSG_ERR_GENERIC.format('91', 'No [type] argument provided')
                flag = False

            #functions database operations
            if flag is False:
                print Language.MSG_ERR_GENERIC.format("95", "SQL command could not be created")
            else:
                results = self.db.select(cmd)
                if results:
                    try:
                        for row in results:
                            for r in row:
                                print r, '\n'
                    except Exception as e:
                        print e.message
                else:
                    raise Exception(Language.MSG_ERR_GENERIC.format(self.utils.get_line(), "Cmd not created"))
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    def group(self, args):
        """
            add new group with params
        """
        #group = Group()
        try:
            params = self.argparser.get_args(args)
            #check namespace variables if set
            if params.name is Empty:
                print Language.MSG_ERR_EMPTY_NAME.format('group')
            else:
                group.setName(params.name)
            if params.config is Empty:
                print Language.MSG_ERR_EMPTY_CONFIG.format('group')
            else:
                group.setConfig(params.config)
            cmd = SQL.SQL_INSERT_GROUP.format(
                group.getName(),
                group.getConfig(),
                self.now,
                self.now
            )
            id = self.db.insert(cmd)
            if id is Empty:
                print Language.MSG_ERR_DATABASE_ERROR.format('128', 'inserting new group', id)
            else:
                print Language.MSG_ADD_NEW.format('group', id, group.getName())
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format("133", e.message)
            pass

    def configure(self, args):
        """
        """
        print ""

    def show(self, args):
        """
        """

    def vlan(self, args):
        """
        """

    def set(self, args):
        """


        :param args:
        """

    def remove(self, args):
        """
            remove device from inventory
        :param args:
        """
        id = None
        name = None
        cmd = None

        try:
            params = self.argparser.get_args(args)
            #check namespace variables if set
            type = params.type
            #moderate type value to determine the statement
            #check if type is group to remove the group belong to given id and name
            if type == 'group':
                if params.id is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('id'), '\n'
                    print Language.MSG_ADD_ID_HELP
                elif params.name is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('name'), '\n'
                    print Language.MSG_ADD_NAME_HELP
                else:
                    id = params.id
                    name = params.name
                    cmd = SQL.SQL_REMOVE_GROUP.format(name, id)
            #check if type is device to remove the group belong to given id and name
            elif type == 'device':
                if params.id is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('id'), '\n'
                    print Language.MSG_ADD_ID_HELP
                elif params.name is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('name'), '\n'
                    print Language.MSG_ADD_NAME_HELP
                else:
                    id = params.id
                    name = params.name
                    cmd = SQL.SQL_REMOVE_DEVICE.format(name, id)
            elif type == 'config':
                if params.name is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('name'), '\n'
                    print Language.MSG_ADD_NAME_HELP
                else:
                    id = params.id
                    cmd = SQL.SQL_INSERT_CONFIG.format(name)
            elif type == 'from':
                cmd = SQL.SQL_REMOVE_DEVICE_FROM_GROUP
            elif type == 'vlan':
                if params.id is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('id'), '\n'
                    print Language.MSG_ADD_ID_HELP
                else:
                    id = params.id
                    cmd = SQL.SQL_REMOVE_VLAN.format(id)
            else:
                print Language.MSG_ERR_GENERIC.format('186', 'No [type] argument provided')

            #functions database operations
            if cmd is Empty:
                print Language.MSG_ERR_GENERIC.format("222", "SQL command could not be created")
            else:
                self.db.remove(cmd)
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format("133", e.message)
            pass

    def help(self, args):
        """

        :param args:
        """
        #formatter = parser._get_formatter()
        #parser.exit(message=formatter.format_help())
        print Language.MSG_ARG_DESC
