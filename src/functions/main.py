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
        deviceMethods = DeviceMethods()
        configMethods = ConfigMethods()
        groupMethods = GroupMethods()
        vlanMethods = VLanMethods()
        try:
            arglist = self.utils.getCleanParams(args)
            params = self.argparser.get_args(arglist)
            if params:
                pType = params.type.split()[0]
                # noinspection PyArgumentList
                if pType == 'device':
                    # noinspection PyArgumentList
                    deviceMethods.create(params)
                elif pType == 'group':
                    # noinspection PyArgumentList
                    groupMethods.create(params)
                elif pType == 'config':
                    # noinspection PyArgumentList
                    configMethods.create(params)
                elif pType == 'vlan':
                    vlanMethods.create(params)
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
        deviceMethods = DeviceMethods()
        configMethods = ConfigMethods()
        groupMethods = GroupMethods()
        vlanMethods = VLanMethods()
        try:
            arglist = self.utils.getCleanParams(args)
            params = self.argparser.get_args(arglist)
            if params:
                pType = params.type.split()[0]
                # noinspection PyArgumentList
                if pType == 'device':
                    # noinspection PyArgumentList
                    deviceMethods.update(params)
                elif pType == 'group':
                    # noinspection PyArgumentList
                    groupMethods.update(params)
                elif pType == 'config':
                    # noinspection PyArgumentList
                    configMethods.update(params)
                elif pType == 'vlan':
                    vlanMethods.update(params)
                else:
                    print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No [type] argument provided')
            else:
                raise Exception("Something wrong with type")
                pass
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
        cmd = None

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
            Add device(s) or given type to group with params
        :param args:
        """
        try:
            arglist = self.utils.getCleanParams(args)
            params = self.argparser.get_args(arglist)
            if params:
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
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    #this method works fine do not touch it!!!
    def show(self, args):
        """
            This method show running configuration by given option
        :param args:
        """
        deviceMethods = DeviceMethods()
        configMethods = ConfigMethods()
        groupMethods = GroupMethods()
        vlanMethods = VLanMethods()
        try:
            #moderate type value to determine the statement
            arglist = self.utils.getCleanParams(args)
            params = self.argparser.get_args(arglist)
            if params:
                pType = params.type.split()[0]
                # noinspection PyArgumentList
                if pType == 'device':
                    # noinspection PyArgumentList
                    deviceMethods.show(params)
                elif pType == 'group':
                    # noinspection PyArgumentList
                    groupMethods.show(params)
                elif pType == 'config':
                    # noinspection PyArgumentList
                    configMethods.show(params)
                elif pType == 'vlan':
                    vlanMethods.show(params)
                else:
                    print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No [type] argument provided')
        except Exception as e:
            print str(e)
            pass

    #this method works fine do not touch it!!!
    def set(self, args):
        """
        This method enables to set the device by given variables such as ssid, channel, frequency, maxclient
        :param args:
        """
        deviceMethods = DeviceMethods()
        configMethods = ConfigMethods()
        groupMethods = GroupMethods()
        vlanMethods = VLanMethods()
        try:
            #moderate type value to determine the statement
            arglist = self.utils.getCleanParams(args)
            params = self.argparser.get_args(arglist)
            if params:
                pType = params.type.split()[0]
                # noinspection PyArgumentList
                if pType == 'device':
                    # noinspection PyArgumentList
                    deviceMethods.set(params)
                elif pType == 'group':
                    # noinspection PyArgumentList
                    groupMethods.set(params)
                elif pType == 'config':
                    # noinspection PyArgumentList
                    configMethods.create(params)
                elif pType == 'vlan':
                    vlanMethods.create(params)
                else:
                    print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No [type] argument provided')
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
            arglist = self.utils.getCleanParams(args)
            params = self.argparser.get_args(arglist)
            #check namespace variables if set
            #moderate type value to determine the statement
            #check if type is group to remove the group belong to given id and name
            if params:
                pType = params.type.split()[0]
                #set gathered id params to be used
                if params.id:
                    pID = params.id
                elif params.name:
                    pName = params.name
                else:
                    print Language.MSG_ERR_EMPTY_ID + '\n' + Language.MSG_ERR_EMPTY_NAME

                if pType and pID or pName:
                    if pType == 'group':
                        cmd = SQL.SQL_REMOVE_GROUP % {'id': int(pID)}

                    #check if type is device to remove the group belong to given id and name
                    elif pType == 'device':
                        cmd = SQL.SQL_REMOVE_DEVICE % {'id': int(pID)}

                    #check if type is config to remove the group belong to given id and name
                    elif pType == 'config':
                        cmd = SQL.SQL_REMOVE_CONFIG % {'id': int(pID)}
                    #remove from given device from given group
                    elif pType == 'from':
                        cmd = SQL.SQL_REMOVE_DEVICE_FROM_GROUP % {'device': int(pID), 'group': ''}

                    #remove vlan record from database
                    elif pType == 'vlan':
                        cmd = SQL.SQL_REMOVE_VLAN % {'id': int(pID)}
                    else:
                        print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), 'No [type] argument provided')

            #functions database operations
            if cmd is Empty:
                print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), "SQL command could not be created")
            else:
                self.db.remove(cmd)
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
            Language.MSG_ADD_GROUP_HELP,
            Language.MSG_ADD_CONFIG,
            Language.MSG_ADD_SUBNET_HELP,
            Language.MSG_ADD_DEVICE_HELP,
            Language.MSG_ADD_DESC_HELP,
            Language.MSG_ADD_RADIUS_HELP,
            Language.MSG_ADD_SSID_HELP,
            Language.MSG_ADD_VLAN_HELP,
            Language.MSG_ADD_CHANNEL_HELP,
            Language.MSG_ADD_FREQ_HELP,
            Language.MSG_ADD_TYPE_HELP,
            Language.MSG_ADD_OPTION_HELP
        )
