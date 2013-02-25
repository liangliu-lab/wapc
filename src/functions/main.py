# coding=utf-8

"""
    Documentation
    :author Fatih Karatana
"""

from Queue import Empty
from time import strftime, gmtime
from src.config.__sql__ import SQL
from src.database.db import Database
from src.functions.VLanMethods import VLanMethods
from src.helper.ArgParser import ArgParser
from src.helper.Utils import Utils
from src.language.language import Language
from src.resources.resources import Resources
from src.functions.DeviceMethods import DeviceMethods
from src.functions.GroupMethods import GroupMethods
from src.functions.ConfigMethods import ConfigMethods

__author__ = 'fatih'


class Main(object):
    """
        Main class includes all base functions of the software
    """

    def __init__(self):
        self.deviceMethods = DeviceMethods()
        self.configMethods = ConfigMethods()
        self.groupMethods = GroupMethods()
        self.vlanMethods = VLanMethods()
        self.utils = Utils()
        self.argparser = ArgParser()
        self.now = strftime(Resources.time_format, gmtime())
        self.db = Database()

    #this methods works fine do not touch it!!!
    def add(self, args):
        """
            Add any object to the related tables such as new wireless access point, group, configuration, vlan etc.
        :rtype : object
        :param args:
        """
        try:
            arglist = self.utils.getCleanParams(args)
            params = self.argparser.get_args(arglist)
            if params:
                pType = params.type.split()[0]
                # noinspection PyArgumentList
                if pType == 'device':
                    # noinspection PyArgumentList
                    self.deviceMethods.create(params)
                elif pType == 'group':
                    # noinspection PyArgumentList
                    self.groupMethods.create(params)
                elif pType == 'config':
                    # noinspection PyArgumentList
                    self.configMethods.create(params)
                elif pType == 'vlan':
                    self.vlanMethods.create(params)
                else:
                    print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No [type] argument provided')
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    #this methods works fine do not touch it!!!
    def edit(self, args):
        """
            Edit any object to the related tables such as new wireless access point, group, configuration, vlan etc.
        :param args:
        """
        try:
            arglist = self.utils.getCleanParams(args)
            params = self.argparser.get_args(arglist)
            if params:
                pType = params.type.split()[0]
                # noinspection PyArgumentList
                if pType == 'device':
                    # noinspection PyArgumentList
                    self.deviceMethods.update(params)
                elif pType == 'group':
                    # noinspection PyArgumentList
                    self.groupMethods.update(params)
                elif pType == 'config':
                    # noinspection PyArgumentList
                    ConfigMethods.update(params)
                elif pType == 'vlan':
                    self.vlanMethods.update(params)
                else:
                    print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No [type] argument provided')
            else:
                raise Exception("Something wrong with type")
                pass
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    #this methods works fine do not touch it!!!
    def list(self, args):
        """
        Remove any record from the inventory by given
        type and values such as device, group and id to decribe the record
        :param args:
        """
        cmd = None
        flag = False

        try:
            arglist = self.utils.getCleanParams(args)
            params = self.argparser.get_args(arglist)
            #check namespace variables if set
            pType = params.type.split()[0]
            #moderate type value to determine the statement
            if pType == 'group':
                cmd = SQL.SQL_SELECT_GROUP_ALL
                flag = True
            elif pType == 'device':
                cmd = SQL.SQL_SELECT_DEVICE_ALL
                flag = True
            elif pType == 'config':
                cmd = SQL.SQL_SELECT_CONFIG
                flag = True
            elif pType == 'vlan':
                cmd = SQL.SQL_SELECT_VLAN
                flag = True
            else:
                print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No [type] argument provided')
                flag = False

            #functions database operations
            if flag is False:
                print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), "SQL command could not be created")
            else:
                fields, results = self.db.select(cmd)
                if fields and results:
                    try:
                        self.utils.formatter(fields, results)
                    except Exception as e:
                        print e.message
                        pass
                else:
                    raise Exception(
                        Language.MSG_ERR_GENERIC.format(self.utils.get_line(), "There is no record found on table"))
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    def group(self, args):
        """
            Add device(s) to group with params
        :param args:
        """
        try:
            arglist = self.utils.getCleanParams(args)
            params = self.argparser.get_args(arglist)
            #check namespace variables if set
            #pType = params.type.split()[0]
            #moderate type value to determine the statement
            if params:
                #pType = params.type.split()[0]
                # noinspection PyArgumentList
                #group given items
                print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No [type] argument provided')
            else:
                raise Exception("Something wrong with type")
                pass
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    def configure(self, args):
        """

        :param args:
        """
        print ""

    def show(self, args):
        """

        :param args:
        """

    def set(self, args):
        """
        This method enables to set the device by given variables such as ssid, channel, frequency, maxclient
        :param args:
        """
        try:
            #moderate type value to determine the statement
            arglist = self.utils.getCleanParams(args)
            params = self.argparser.get_args(arglist)
            if params:
                pType = params.type.split()[0]
                # noinspection PyArgumentList
                if pType == 'device':
                    # noinspection PyArgumentList
                    self.deviceMethods.set(params)
                elif pType == 'group':
                    # noinspection PyArgumentList
                    self.groupMethods.create(params)
                elif pType == 'config':
                    # noinspection PyArgumentList
                    self.configMethods.create(params)
                elif pType == 'vlan':
                    self.vlanMethods.create(params)
                else:
                    print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No [type] argument provided')
        except Exception as e:
            print str(e)
            pass

    def remove(self, args):
        """
        Remove any record from the inventory by given
        type and values such as device, group and id to decribe the record
        :param args:
        """
        pid = None
        name = None
        cmd = None

        try:
            arglist = self.utils.getCleanParams(args)
            params = self.argparser.get_args(arglist)
            #check namespace variables if set
            pType = params.type.split()[0]
            #moderate type value to determine the statement
            #check if type is group to remove the group belong to given id and name
            if pType == 'group':
                if params.id is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('id'), '\n'
                    print Language.MSG_ADD_ID_HELP
                elif params.name is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('name'), '\n'
                    print Language.MSG_ADD_NAME_HELP
                else:
                    pid = params.id
                    name = params.name
                    cmd = SQL.SQL_REMOVE_GROUP.format(name, pid)
            #check if type is device to remove the group belong to given id and name
            elif pType == 'device':
                if params.id is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('id'), '\n'
                    print Language.MSG_ADD_ID_HELP
                elif params.name is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('name'), '\n'
                    print Language.MSG_ADD_NAME_HELP
                else:
                    pid = params.id
                    name = params.name
                    cmd = SQL.SQL_REMOVE_DEVICE.format(name, pid)
            elif pType == 'config':
                if params.name is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('name'), '\n'
                    print Language.MSG_ADD_NAME_HELP
                else:
                    #pid = params.id
                    cmd = SQL.SQL_INSERT_CONFIG.format(name)
            elif pType == 'from':
                cmd = SQL.SQL_REMOVE_DEVICE_FROM_GROUP
            elif pType == 'vlan':
                if params.id is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('id'), '\n'
                    print Language.MSG_ADD_ID_HELP
                else:
                    pid = params.id
                    cmd = SQL.SQL_REMOVE_VLAN.format(pid)
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
