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

@package controller
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology
"""
import socket

from time import strftime, gmtime
from src.controller.Logger import Logger
from src.resources.SQL import SQL
from src.database.Database import Database
from src.controller.VLanMethods import VLanMethods
from src.helpers.ArgParser import ArgParser
from src.helpers.Utils import Utils
from src.language.Language import Language
from src.model.Config import Config
from src.resources.Resources import Resources
from src.controller.DeviceMethods import DeviceMethods
from src.controller.GroupMethods import GroupMethods
from src.controller.ConfigMethods import ConfigMethods

__author__ = 'fatih'


class Main(object):
    """
    Main class handles main requires and distribute them into related
    subprocesses. This class is called by ConsoleInterface and communicate
    with sub-controllers. Main class also manipulate commandline arguments, clear
    them from whitespaces, apply a filter regex and send them into ArgParser.

    @author Fatih Karatana
    """
    #test and production
    def __init__(self):
        self.utils = Utils()
        self.arg_parser = ArgParser()
        self.now = strftime(Resources.time_format, gmtime())
        self.database = Database(self.utils.master_db)
        self.logger = Logger()
        #self.daemon.start()

    #this methods works fine do not touch it!!!
    def add(self, args):
        """
        Add any object to the related tables such as new wireless access
        point, group, configuration, vlan etc.

        @param args
        """
        try:

            if args:
                arg_list = self.utils.get_clean_params(args)
                params = self.arg_parser.get_args(arg_list)
                device_methods = DeviceMethods(params)
                config_methods = ConfigMethods(Config(), params)
                group_methods = GroupMethods()
                vlan_methods = VLanMethods()

                if params.type and self.utils.type_exists(params.type):
                    param_type = str(params.type.strip()).lower()
                else:
                    param_type = raw_input(
                        "Please provide a type argument "
                        "[device/group/config/vlan]:").strip()
                    if not param_type:
                        param_type = 'device'

                # noinspection PyArgumentList
                if param_type == 'device':
                    # noinspection PyArgumentList
                    device_methods.create(params)
                elif param_type == 'group':
                    # noinspection PyArgumentList
                    group_methods.create(params)
                elif param_type == 'config':
                    # noinspection PyArgumentList
                    config_methods.create(params)
                elif param_type == 'vlan':
                    vlan_methods.create(params)
                else:
                    raise BaseException(Language.MSG_ERR_TYPE_ARGUMENT_PROVIDED)
            else:
                raise BaseException(Language.MSG_ERR_ARGUMENT_PROVIDED)
        except BaseException as exception:
            raise BaseException(exception.message)

    #this methods works fine do not touch it!!!
    def edit(self, args):
        """
        Edit any object to the related tables such as new wireless
        access point, group, configuration, vlan etc.

        @param args
        """
        try:
            if args:
                arg_list = self.utils.get_clean_params(args)
                params = self.arg_parser.get_args(arg_list)
                device_methods = DeviceMethods(params)
                config_methods = ConfigMethods(Config(), params)
                group_methods = GroupMethods()
                vlan_methods = VLanMethods()
                if params.type and self.utils.type_exists(params.type):
                    param_type = str(params.type.strip()).lower()
                else:
                    param_type = raw_input(
                        "Please provide a type argument "
                        "[device/group/config/vlan]:").strip()
                    if not param_type:
                        param_type = 'device'

                # noinspection PyArgumentList
                if param_type == 'device':
                    # noinspection PyArgumentList
                    device_methods.update(params)
                elif param_type == 'group':
                    # noinspection PyArgumentList
                    group_methods.update(params)
                elif param_type == 'config':
                    # noinspection PyArgumentList
                    config_methods.update(params)
                elif param_type == 'vlan':
                    vlan_methods.update(params)
                else:
                    print Language.MSG_ERR_GENERIC.format(
                        self.utils.get_line(), 'No [type] argument provided')
            else:
                raise BaseException(Language.MSG_ERR_ARGUMENT_PROVIDED)
        except BaseException as exception:
            raise BaseException(exception.message)

    #this method works fine do not touch it!!!
    def list(self, args):
        """
        List all record from the inventory by given
        type and values such as device, group and id to decribe the record

        @param args:
        """
        try:
            if args:
                arg_list = self.utils.get_clean_params(args)
                params = self.arg_parser.get_args(arg_list)
                #check namespace variables if set
                if params.type and self.utils.type_exists(params.type):
                    param_type = str(params.type.strip()).lower()
                else:
                    param_type = raw_input(
                        "Please provide a type argument "
                        "[device/group/config/vlan]:").strip()
                    if not param_type:
                        param_type = 'device'

                #moderate type value to determine the statement
                if param_type == 'group':
                    cmd = SQL.SQL_SELECT_GROUP_ALL
                elif param_type == 'device':
                    if params.group:
                        cmd = SQL.SQL_SELECT_DEVICE_FROM_GROUP % {
                            'group_id': int(params.group.strip())}
                    elif not params.group and params.id:
                        cmd = SQL.SQL_SELECT_DEVICE % {'id': int(params.id)}
                    else:
                        cmd = SQL.SQL_SELECT_DEVICE_ALL
                elif param_type == 'config':
                    cmd = SQL.SQL_SELECT_CONFIG
                elif param_type == 'vlan':
                    cmd = SQL.SQL_SELECT_VLAN
                else:
                    raise TypeError(
                        Language.MSG_ERR_GENERIC.format(
                            self.utils.get_line(),
                            'No or wrong [type] argument provided')
                    )

                fields, results = self.database.select(cmd)
                if fields and results:
                    self.utils.formatter(fields, results)
                else:
                    print "There is no record found on table"
                    self.logger.create_log(
                        name="Base Exception",
                        severity=self.logger.severity.INFO,
                        line=self.utils.get_line(),
                        message=Language.MSG_ERR_GENERIC.format(
                            self.utils.get_line(),
                            "There is no record found on table"),
                        method="edit",
                        facility="Main.edit",
                        host=socket.gethostname()
                    )
            else:
                raise BaseException(Language.MSG_ERR_ARGUMENT_PROVIDED)
        except BaseException as exception:
            raise BaseException(exception.message)

    def group(self, args):
        """
        Add device(s) or given type to group with params

        @param args:
        """
        device_id = None
        group_id = None
        try:
            if args:
                arg_list = self.utils.get_clean_params(args)
                params = self.arg_parser.get_args(arg_list)
                if params.id and params.group:
                    device_id = params.id
                    group_id = params.group
                elif not params.id:
                    print Language.MSG_ERR_EMPTY_ID.format('device')
                    device_id = raw_input(Language.MSG_ADD_ID_HELP)
                elif not params.group:
                    print Language.MSG_ADD_GROUP_HELP.format('device')
                    group_id = raw_input(Language.MSG_ADD_GROUP_HELP)

                if device_id and group_id:
                    cmd = SQL.SQL_INSERT_DEVICE_TO_GROUP % {
                        'device_id': int(device_id),
                        'group_id': int(group_id),
                        'added': self.now,
                        'modified': self.now
                    }
                    self.database.insert(cmd)
                    print Language.MSG_SUCCESS_ADD
                else:
                    raise TypeError(
                        Language.MSG_ERR_GENERIC.format(
                            self.utils.get_line(),
                            'Device id and group id could not be gathered\n'
                            'Please try again to execute command'
                        )
                    )
            else:
                raise BaseException(Language.MSG_ERR_ARGUMENT_PROVIDED)
        except BaseException as exception:
            raise BaseException(exception.message)

    #this method works fine do not touch it!!!
    def show(self, args):
        """
        This method show running configuration by given option
        Required parameters are type, option, and id

        @param args
        """
        try:
            #moderate type value to determine the statement
            if args:
                arg_list = self.utils.get_clean_params(args)
                params = self.arg_parser.get_args(arg_list)
                params.command = "show"
                device_methods = DeviceMethods(params)
                config_methods = ConfigMethods(Config(), params)
                group_methods = GroupMethods()
                vlan_methods = VLanMethods()

                if params.type and self.utils.type_exists(params.type):
                    param_type = str(params.type.strip()).lower()
                else:
                    param_type = raw_input(
                        "Please provide a type argument "
                        "[device/group/config/vlan]:").strip()
                    if not param_type:
                        param_type = 'device'

                if not params.option:
                    print Language.MSG_ERR_EMPTY_OPTION.format('device')
                    option = raw_input(Language.MSG_INPUT_PARAM_OPTION %
                                       {'param': 'option'})
                    params.option = option

                # noinspection PyArgumentList
                if param_type == 'device':
                    # noinspection PyArgumentList
                    if self.utils.command_exists(params):
                        print device_methods.show(params)
                    else:
                        print "You provided a command which is not in device " \
                              "command json file.\nPlease check the option " \
                              "'%s' then try again your command" % params.option
                elif param_type == 'group':
                    # noinspection PyArgumentList
                    if self.utils.command_exists(params):
                        print group_methods.show(params)
                    else:
                        print "You provided a command which is not in device " \
                              "command json file.\nPlease check the option " \
                              "'%s' then try again your command" % params.option
                elif param_type == 'config':
                    # noinspection PyArgumentList
                    config_methods.show(params)
                elif param_type == 'vlan':
                    vlan_methods.show(params)
                else:
                    raise BaseException(
                        Language.MSG_ERR_GENERIC.format(
                            self.utils.get_line(),
                            'No [type] argument provided'
                        )
                    )
            else:
                raise BaseException(Language.MSG_ERR_ARGUMENT_PROVIDED)
        except BaseException as exception:
            raise BaseException(exception.message)

    #this method works fine do not touch it!!!
    def set(self, args):
        """
        This method enables to set the device by given variables such as ssid,
        channel, frequency, maxclient

        @param args
        """
        try:
            #moderate type value to determine the statement
            if args:
                arg_list = self.utils.get_clean_params(args)
                params = self.arg_parser.get_args(arg_list)
                params.command = "set"
                device_methods = DeviceMethods(params)
                config_methods = ConfigMethods(Config(), params)
                group_methods = GroupMethods()
                vlan_methods = VLanMethods()
                param_type = params.type.split()[0]
                # noinspection PyArgumentList
                if param_type == 'device':
                    # noinspection PyArgumentList
                    device_methods.set(params)
                elif param_type == 'group':
                    # noinspection PyArgumentList
                    group_methods.set(params)
                elif param_type == 'config':
                    # noinspection PyArgumentList
                    config_methods.create(params)
                elif param_type == 'vlan':
                    vlan_methods.create(params)
                else:
                    raise TypeError(
                        Language.MSG_ERR_GENERIC.format(
                            self.utils.get_line(),
                            'No [type] argument provided'
                        )
                    )
            else:
                raise BaseException(Language.MSG_ERR_ARGUMENT_PROVIDED)
        except BaseException as exception:
            raise BaseException(exception.message)

    #this method works fine do not touch it!!!
    def unset(self, args):
        """
        This method enables to unset the device by given variables such as ssid,
        channel, frequency, maxclient

        @param args
        """
        try:
            #moderate type value to determine the statement
            if args:
                arg_list = self.utils.get_clean_params(args)
                params = self.arg_parser.get_args(arg_list)
                params.command = "unset"
                device_methods = DeviceMethods(params)
                group_methods = GroupMethods()
                param_type = params.type.split()[0]
                # noinspection PyArgumentList
                if param_type == 'device':
                    # noinspection PyArgumentList
                    params.command = "unset"
                    device_methods.set(params)
                elif param_type == 'group':
                    # noinspection PyArgumentList
                    group_methods.unset(params)
                else:
                    raise TypeError(
                        Language.MSG_ERR_GENERIC.format(
                            self.utils.get_line(),
                            'No [type] argument provided'
                        )
                    )
            else:
                raise BaseException(Language.MSG_ERR_ARGUMENT_PROVIDED)
        except BaseException as exception:
            raise BaseException(exception.message)

    #this method works fine do not touch it!!!
    def remove(self, args):
        """
        Remove any record from the inventory by given
        type and values such as device, group and id to decribe the record

        @param args
        """
        param_name = None
        param_id = None
        cmd = None

        try:
            if args:
                arg_list = self.utils.get_clean_params(args)
                params = self.arg_parser.get_args(arg_list)

                #set gathered id params to be used
                if params.type:
                    param_type = params.type.split()[0]
                    param_type = str(param_type).lower()
                else:
                    param_type = raw_input("Please provide a type:")\
                        .strip()
                    param_type = str(param_type).lower()

                if params.id:
                    param_id = params.id.strip()
                elif params.name:
                    param_name = params.name.strip()
                else:
                    print Language.MSG_ERR_EMPTY_ID + \
                          '\n' + Language.MSG_ERR_EMPTY_NAME

                if param_type and param_id or param_name:
                    if param_type == 'group':
                        cmd = SQL.SQL_REMOVE_GROUP % {'id': int(param_id)}

                    #check if type is device to remove the group
                    # belong to given id and name
                    elif param_type == 'device':
                        cmd = SQL.SQL_REMOVE_DEVICE % {'id': int(param_id)}

                    #check if type is config to remove the group
                    # belong to given id and name
                    elif param_type == 'config':
                        cmd = SQL.SQL_REMOVE_CONFIG % {'id': int(param_id)}

                    #remove from given device from given group
                    elif param_type == 'from':
                        if params.group:
                            group_id = params.group.rstrip().lstrip()
                            cmd = SQL.SQL_REMOVE_DEVICE_FROM_GROUP % {
                                'device': int(param_id), 'group': int(group_id)}
                        else:
                            raise Exception(
                                Language.MSG_ERR_EMPTY_GROUP
                            )

                    #remove vlan record from database
                    elif param_type == 'vlan':
                        cmd = SQL.SQL_REMOVE_VLAN % {'id': int(param_id)}
                    else:
                        raise BaseException("No [type] argument provided")

                if cmd:
                    self.database.remove(cmd)
                    self.logger.create_log(
                        name="Shell.py Exception",
                        severity=self.logger.severity.INFO,
                        line=self.utils.get_line(),
                        message="Given %(type)s",
                        method="__main__",
                        facility="shell.main",
                        host=socket.gethostname()
                    )
                else:
                    raise BaseException("SQL command could not be created")

            else:
                raise BaseException(Language.MSG_ERR_ARGUMENT_PROVIDED)
        except BaseException as exception:
            raise BaseException(exception.message)

    #this method works fine do not touch it!!!
    @classmethod
    def help(cls, args):
        """
        Print help text

        @param cls class itself
        @param args
        """
        #formatter = parser._get_formatter()
        #parser.exit(message=formatter.format_help())
        del args
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
