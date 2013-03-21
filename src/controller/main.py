# coding=utf-8

"""
    Main class handles main requires and distribute them into related subprocesses. This class is called by
    @class ConsoleInterface() and communicate with sub-controllers. Main class also manipulate commandline arguments,
    clear them from whitespaces, apply a filter regex and send them into @class ArgParser().

    @author Fatih Karatana
"""

from time import strftime, gmtime
from src.config.__sql__ import SQL
from src.database.db import Database
from src.controller.VLanMethods import VLanMethods
from src.helper.ArgParser import ArgParser
from src.helper.Utils import Utils
from src.language.language import Language
from src.model.Config import Config
from src.resources.resources import Resources
from src.controller.DeviceMethods import DeviceMethods
from src.controller.GroupMethods import GroupMethods
from src.controller.ConfigMethods import ConfigMethods

__author__ = 'fatih'


class Main(object):
    """
        Main class includes all base controller methods of the software
    """
    # TODO create an environment to make software work as in development, test and production
    def __init__(self):
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

            if args:
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
                deviceMethods = DeviceMethods(params)
                configMethods = ConfigMethods(Config(), params)
                groupMethods = GroupMethods()
                vlanMethods = VLanMethods()
                pType = params.type.split()[0]
                # noinspection PyArgumentList
                if str(pType).lower() == 'device':
                    # noinspection PyArgumentList
                    deviceMethods.create(params)
                elif str(pType).lower() == 'group':
                    # noinspection PyArgumentList
                    groupMethods.create(params)
                elif str(pType).lower() == 'config':
                    # noinspection PyArgumentList
                    configMethods.create(params)
                elif str(pType).lower() == 'vlan':
                    vlanMethods.create(params)
                else:
                    print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No [type] argument provided')
            else:
                print Language.MSG_CMD_ADD_HELP
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
            if args:
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
                deviceMethods = DeviceMethods(params)
                configMethods = ConfigMethods(Config(), params)
                groupMethods = GroupMethods()
                vlanMethods = VLanMethods()
                pType = params.type.split()[0]
                # noinspection PyArgumentList
                if str(pType).lower() == 'device':
                    # noinspection PyArgumentList
                    deviceMethods.update(params)
                elif str(pType).lower() == 'group':
                    # noinspection PyArgumentList
                    groupMethods.update(params)
                elif str(pType).lower() == 'config':
                    # noinspection PyArgumentList
                    configMethods.update(params)
                elif str(pType).lower() == 'vlan':
                    vlanMethods.update(params)
                else:
                    print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No [type] argument provided')
            else:
                print Language.MSG_CMD_EDIT_HELP
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    #this method works fine do not touch it!!!
    def list(self, args):
        """
        List all record from the inventory by given
        type and values such as device, group and id to decribe the record
        :param args:
        """
        try:
            if args:
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
                #check namespace variables if set
                pType = params.type.split()[0]
                #moderate type value to determine the statement
                if str(pType).lower() == 'group':
                    cmd = SQL.SQL_SELECT_GROUP_ALL
                elif str(pType).lower() == 'device':
                    if params.group:
                        cmd = SQL.SQL_SELECT_DEVICE_FROM_GROUP % {'group_id': int(params.group.strip())}
                    elif not params.group and params.id:
                        cmd = SQL.SQL_SELECT_DEVICE % {'id':int(params.id)}
                    else:
                        cmd = SQL.SQL_SELECT_DEVICE_ALL
                elif str(pType).lower() == 'config':
                    cmd = SQL.SQL_SELECT_CONFIG
                elif str(pType).lower() == 'vlan':
                    cmd = SQL.SQL_SELECT_VLAN
                else:
                    raise Exception(
                        Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No or wrong [type] argument provided')
                    )

                if cmd:
                    fields, results = self.db.select(cmd)
                    if fields and results:
                        self.utils.formatter(fields, results)
                    else:
                        raise Exception(
                            Language.MSG_ERR_GENERIC.format(self.utils.get_line(), "There is no record found on table"))
                else:
                    print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), "SQL command could not be created")

            else:
                print Language.MSG_CMD_LIST_HELP
        except Exception as e:
            print e.message
            pass

    def group(self, args):
        """
            Add device(s) or given type to group with params
        :param args:
        """
        try:

            if args:
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
                if params.id and params.group:
                    dID = params.id
                    gID = params.group
                    cmd = SQL.SQL_INSERT_DEVICE_TO_GROUP % {
                        'device_id': int(dID),
                        'group_id': int(gID),
                        'added': self.now,
                        'modified': self.now
                    }
                    self.db.insert(cmd)
                    print Language.MSG_SUCCESS_ADD
                else:
                    print Language.MSG_ERR_EMPTY_ID.format('device')
                    pass
            else:
                print Language.MSG_CMD_GROUP_HELP
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    #this method works fine do not touch it!!!
    def show(self, args):
        """
            This method show running configuration by given option
        :param args:
        """
        try:
            #moderate type value to determine the statement
            if args:
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
                deviceMethods = DeviceMethods(params)
                configMethods = ConfigMethods(Config(), params)
                groupMethods = GroupMethods()
                vlanMethods = VLanMethods()
                pType = params.type.split()[0]
                # noinspection PyArgumentList
                if str(pType).lower() == 'device':
                    # noinspection PyArgumentList
                    deviceMethods.show(params)
                elif str(pType).lower() == 'group':
                    # noinspection PyArgumentList
                    groupMethods.show(params)
                elif str(pType).lower() == 'config':
                    # noinspection PyArgumentList
                    configMethods.show(params)
                elif str(pType).lower() == 'vlan':
                    vlanMethods.show(params)
                else:
                    print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No [type] argument provided')
            else:
                print Language.MSG_CMD_SHOW_HELP
        except Exception as e:
            print str(e)
            pass

    #this method works fine do not touch it!!!
    def set(self, args):
        """
        This method enables to set the device by given variables such as ssid, channel, frequency, maxclient
        :param args:
        """
        try:
            #moderate type value to determine the statement
            if args:
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
                deviceMethods = DeviceMethods(params)
                configMethods = ConfigMethods(Config(), params)
                groupMethods = GroupMethods()
                vlanMethods = VLanMethods()
                pType = params.type.split()[0]
                # noinspection PyArgumentList
                if str(pType).lower() == 'device':
                    # noinspection PyArgumentList
                    deviceMethods.set(params)
                elif str(pType).lower() == 'group':
                    # noinspection PyArgumentList
                    groupMethods.set(params)
                elif str(pType).lower() == 'config':
                    # noinspection PyArgumentList
                    configMethods.create(params)
                elif str(pType).lower() == 'vlan':
                    vlanMethods.create(params)
                else:
                    print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No [type] argument provided')
            else:
                print Language.MSG_CMD_SET_HELP
        except Exception as e:
            print str(e)
            pass

    #this method works fine do not touch it!!!
    def unset(self, args):
        """
        This method enables to set the device by given variables such as ssid, channel, frequency, maxclient
        :param args:
        """
        try:
            #moderate type value to determine the statement
            if args:
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
                deviceMethods = DeviceMethods(params)
                configMethods = ConfigMethods(Config(), params)
                groupMethods = GroupMethods()
                vlanMethods = VLanMethods()
                pType = params.type.split()[0]
                # noinspection PyArgumentList
                if str(pType).lower() == 'device':
                    # noinspection PyArgumentList
                    deviceMethods.unset(params)
                elif str(pType).lower() == 'group':
                    # noinspection PyArgumentList
                    groupMethods.unset(params)
                elif str(pType).lower() == 'config':
                    # noinspection PyArgumentList
                    configMethods.unset(params)
                elif str(pType).lower() == 'vlan':
                    vlanMethods.unset(params)
                else:
                    print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No [type] argument provided')
            else:
                print Language.MSG_CMD_UNSET_HELP
        except Exception as e:
            print str(e)
            pass

    #this method works fine do not touch it!!!
    def remove(self, args):
        """
        Remove any record from the inventory by given
        type and values such as device, group and id to decribe the record
        :param args:
        """
        pName = None
        pID = None
        cmd = None

        try:
            if args:
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
                pType = params.type.split()[0]
                #set gathered id params to be used
                if params.id:
                    pID = params.id.rstrip().lstrip()
                elif params.name:
                    pName = params.name.rstrip().lstrip()
                else:
                    print Language.MSG_ERR_EMPTY_ID + '\n' + Language.MSG_ERR_EMPTY_NAME

                if pType and pID or pName:
                    if str(pType).lower() == 'group':
                        cmd = SQL.SQL_REMOVE_GROUP % {'id': int(pID)}

                    #check if type is device to remove the group belong to given id and name
                    elif str(pType).lower() == 'device':
                        cmd = SQL.SQL_REMOVE_DEVICE % {'id': int(pID)}

                    #check if type is config to remove the group belong to given id and name
                    elif str(pType).lower() == 'config':
                        cmd = SQL.SQL_REMOVE_CONFIG % {'id': int(pID)}
                    #remove from given device from given group
                    elif str(pType).lower() == 'from':
                        if params.group:
                            gID = params.group.rstrip().lstrip()
                            cmd = SQL.SQL_REMOVE_DEVICE_FROM_GROUP % {'device': int(pID), 'group': int(gID)}
                        else:
                            raise Exception(
                                Language.MSG_ERR_EMPTY_GROUP
                            )

                    #remove vlan record from database
                    elif str(pType).lower() == 'vlan':
                        cmd = SQL.SQL_REMOVE_VLAN % {'id': int(pID)}
                    else:
                        print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No [type] argument provided')
            else:
                print Language.MSG_CMD_REMOVE_HELP
            if cmd:
                self.db.remove(cmd)
            else:
                raise Exception("SQL command could not be created")
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    #this method works fine do not touch it!!!
    def help(self, args):
        """

        :param args:
        """
        #formatter = parser._get_formatter()
        #parser.exit(message=formatter.format_help())
        print Language.MSG_ARG_DESC.format(
            Language.MSG_CMD_ADD_HELP,
            Language.MSG_CMD_EDIT_HELP,
            Language.MSG_CMD_GROUP_HELP,
            Language.MSG_CMD_SET_HELP,
            Language.MSG_CMD_UNSET_HELP,
            Language.MSG_CMD_LIST_HELP,
            Language.MSG_CMD_SHOW_HELP,
            Language.MSG_CMD_REMOVE_HELP,
            Language.MSG_CMD_SELFTEST_HELP,
            Language.MSG_ADD_ID_HELP,
            Language.MSG_ADD_IP_HELP,
            Language.MSG_ADD_NAME_HELP,
            Language.MSG_ADD_USERNAME_HELP,
            Language.MSG_ADD_PASSWORD_HELP,
            Language.MSG_ADD_PARAM_HELP,
            Language.MSG_ADD_GROUP_HELP,
            Language.MSG_ADD_CONFIG,
            Language.MSG_ADD_SUBNET_HELP,
            Language.MSG_ADD_DEVICE_HELP,
            Language.MSG_ADD_DESC_HELP,
            Language.MSG_ADD_RADIUS_HELP,
            Language.MSG_ADD_SSID_HELP,
            Language.MSG_ADD_VLAN_HELP,
            Language.MSG_ADD_CHANNEL_HELP,
            Language.MSG_ADD_TYPE_HELP,
            Language.MSG_ADD_OPTION_HELP
        )
