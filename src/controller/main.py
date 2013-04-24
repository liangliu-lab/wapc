# coding=utf-8

"""
@mainpage Labris Wirelss Access Point Controller v1.0

<h1>DESCRIPTION</h1>

This software has been created to manage wireless acess point controllers with
no brand dependency.

Version 1.0 includes only CLI(Command Line Interface) to manage devices via
Linux-familiar commands such as rm, ls, etc..

Please see commands and options list below.

<h1>FEATURES</h1>
<ul>
<li>Add new devices into the inventory</li>
<li>Create groups with given devices</li>
<li>Manage device configurations, add, update and delete</li>
<li>Manage device SSID, Channel, Associations, Maxclients</li>
<li>Roaming</li>
<li>Group management</li>
<li>Service oriented architecture to communicate devices over Telnet</li>
<li>Configure device commands over wapc-config.json</li>
<</ul>

<h1>COMMAND & OPTIONS</h1>
Use methods below to add, remove, update and list device(s), group(s) or
config(s) with commands:

<h2>Commands:</h2>
<h3>Usage: $ add [OPTIONS]</h3>
Add device, group, vlan, config etc with given parameters
<ul>
<li>[-t],[--type] Define type device, group, vlan, config</li>
<li>[-I],[--ip] Use this params when adding some new variables which needs
an ip such as device, config, etc.</li>
<li>[-n],[--name] To set a name to related type variable</li>
<li>[-b],[--brand] To set device brand to relate with its model and/or 
firmware</li>
<li>[-m],[--model] To set device model to relate with its config file</li>
<li>[-F],[--firmware] To set device firmware to relate with its config file</li>
<li>[-R],[--relation] To set device relation one of MASTER of SLAVE</li>
<li>[-D],[--description] To set a description to related type variable</li>
<li>[-u],[--username] Provide a username which will be used to connect
device</li>
<li>[-p],[--password] Provide a password which will be used to connect and
configure device</li>
</ul>
<h3>Usage: $ edit [OPTIONS]</h3>
Edit details of given type of device with given parameters
<ul>
<li>[-t],[--type] Define type device, group, vlan, config</li>
<li>[-o],[--option] Provide option must be one of related type database 
fields</li>
<li>[-P],[--param] Provide parameter to be update value</li>
</ul>
<h3>Usage: $ group [OPTIONS]</h3>
Group given devices
<ul>
<li>[-t],[--type] Define type device, group, vlan, config</li>
<li>[-g],[--group] Define the group where given device will be added into</li>
<li>[-i],[--id] Define id of device, group, vlan, config</li>
</ul>
<h3>Usage: $ set [OPTIONS]</h3>
Add device, group, vlan, config etc with given parameters
<ul>
<li>[-t],[--type] Define type device, group, vlan, config</li>
<li>[-i],[--id] Define id of device or group</li>
<li>[-o],[--option] Provide option must be one of "ssid, vlan, channel,
frequency, maxclients, ip, cpu, memory, permanent, conf, firmware, model,
serial, clients"</li>
</ul>
These will be used to gather related commands from config file you provided
<h3>Usage: $ unset [OPTIONS]</h3>
Unset option, group, vlan, config etc with given parameters
<ul>
<li>[-t],[--type] Define type device, group, vlan, config</li>
<li>[-i],[--id] Define id of device or group</li>
<li>[-o],[--option] Provide option must be one of</li>
</ul>
"ssid, vlan, channel, frequency, maxclients, ip, cpu, memory, permanent, conf,
firmware, model, serial, clients"
These will be used to gather related commands from config file you provided
<h3>Usage: $ ls [OPTIONS]</h3>
List details of given type
<ul>
<li>[-t],[--type] List device, group, vlan, config</li>
<li>[-g],[--group] List device, vlan or config from given group</li>
<li>[-i],[--id] Define id of group</li>
</ul>
<h3>Usage: $ sh [OPTIONS]</h3>
Show details of given type
<ul>
<li>[-t],[--type] Define type device, group, vlan, config</li>
<li>[-i],[--id] Define id of device or group</li>
<li>[-o],[--option] Provide option must be one of</li>
</ul>
"ssid, vlan, channel, frequency, maxclients, ip, cpu, memory, permanent, conf,
<h3>Usage: $ rm [OPTIONS]</h3>
Show details of given type
<ul>
<li>[-t],[--type] Define type device, group, vlan, config and also it can be
used such asgiven type is from to remove a device from a group</li>
<li>[-g],[--group] Define the group where given device will be remove from</li>
<li>[-i],[--id] Define id of device, group, vlan, config</li>
</ul>
<h3>Usage: $ self [OPTIONS]</h3>
Add device, group, vlan, config etc with given parameters
<ul>
<li>[-t],[--type] Define type device, group, vlan, config</li>
<li>[-I],[--ip] Use this params when adding some new variables which needs an
ip such as device, config, etc.</li>
<li>[-n],[--name] To set a name to related type variable</li>
<li>[-D],[--description] To set a description to related type variable</li>
<li>[-u],[--username] Provide a username which will be used to connect
device</li>
</ul>

<h2>Options:</h2>
<ul>
<li>-i,--id Provide ID address to determine the variable with
usage id</li>
<li>-I,--ip Provide IP address for the newly added device with
usage to connect</li>
<li>-n,--name Provide name for the newly added device with usage name</li>
<li>-u,--username Provide username for the newly added device with
usage username</li>
<li>-p,--password Provide password for given username of the newly
added device with usage password</li>
<li>-P,--param Provide a parameter to be set to the given option</li>
<li>-g,--group Add device to the group with usage group</li>
<li>-c,--config Add new configuration and map it to the given group or 
device</li>
<li>-s,--subnet Define subnet for VLAN will be configured with usage 
255.255.255.0</li>
<li>-d,--device Provide device id to add provided device to the group</li>
<li>-D,--description Provide a short description for group or device
with usage</li>
<li>-r,--radius Provide Radius id to configure radius authentication for 
group or device with usage radius_id</li>
<li>-S,--ssid Provide SSID for group or device with usage ssid</li>
<li>-V,--vlan Provide VLAN id to determine VLAN for group or device with 
usage vlan_id</li>
<li>-H,--channel Provide channel to configure for group or device with 
usage channel</li>
<li>-t,--type Provide type of group/device/config/vlan from database with 
usage group/device/config/vlan others will cause error(s)</li>
<li>-o,--option Provide type of group/device/config/vlan from database with 
usage group/device/config/vlan</li>
</ul>


@section LICENSE
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

@package model
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

<h1>CHANGELOG</h1>
v1.0
"""

from time import strftime, gmtime
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
        self.argparser = ArgParser()
        self.now = strftime(Resources.time_format, gmtime())
        self.database = Database()

    #this methods works fine do not touch it!!!
    def add(self, args):
        """
        Add any object to the related tables such as new wireless access
        point, group, configuration, vlan etc.

        @param args
        """
        try:

            if args:
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
                device_methods = DeviceMethods(params)
                config_methods = ConfigMethods(Config(), params)
                group_methods = GroupMethods()
                vlan_methods = VLanMethods()
                param_type = params.type.split()[0]
                # noinspection PyArgumentList
                if str(param_type).lower() == 'device':
                    # noinspection PyArgumentList
                    device_methods.create(params)
                elif str(param_type).lower() == 'group':
                    # noinspection PyArgumentList
                    group_methods.create(params)
                elif str(param_type).lower() == 'config':
                    # noinspection PyArgumentList
                    config_methods.create(params)
                elif str(param_type).lower() == 'vlan':
                    vlan_methods.create(params)
                else:
                    print Language.MSG_ERR_GENERIC.format(
                        self.utils.get_line(),
                        'No [type] argument provided')
            else:
                print Language.MSG_CMD_ADD_HELP
        except TypeError as exception:
            print exception.message

    #this methods works fine do not touch it!!!
    def edit(self, args):
        """
        Edit any object to the related tables such as new wireless
        access point, group, configuration, vlan etc.

        @param args
        """
        try:
            if args:
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
                device_methods = DeviceMethods(params)
                config_methods = ConfigMethods(Config(), params)
                group_methods = GroupMethods()
                vlan_methods = VLanMethods()
                param_type = params.type.split()[0]
                # noinspection PyArgumentList
                if str(param_type).lower() == 'device':
                    # noinspection PyArgumentList
                    device_methods.update(params)
                elif str(param_type).lower() == 'group':
                    # noinspection PyArgumentList
                    group_methods.update(params)
                elif str(param_type).lower() == 'config':
                    # noinspection PyArgumentList
                    config_methods.update(params)
                elif str(param_type).lower() == 'vlan':
                    vlan_methods.update(params)
                else:
                    print Language.MSG_ERR_GENERIC.format(
                        self.utils.get_line(), 'No [type] argument provided')
            else:
                print Language.MSG_CMD_EDIT_HELP
        except TypeError as exception:
            print exception.message

    #this method works fine do not touch it!!!
    def list(self, args):
        """
        List all record from the inventory by given
        type and values such as device, group and id to decribe the record

        @param args:
        """
        try:
            if args:
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
                #check namespace variables if set
                param_type = params.type.split()[0]
                #moderate type value to determine the statement
                if str(param_type).lower() == 'group':
                    cmd = SQL.SQL_SELECT_GROUP_ALL
                elif str(param_type).lower() == 'device':
                    if params.group:
                        cmd = SQL.SQL_SELECT_DEVICE_FROM_GROUP % {
                            'group_id': int(params.group.strip())}
                    elif not params.group and params.id:
                        cmd = SQL.SQL_SELECT_DEVICE % {'id': int(params.id)}
                    else:
                        cmd = SQL.SQL_SELECT_DEVICE_ALL
                elif str(param_type).lower() == 'config':
                    cmd = SQL.SQL_SELECT_CONFIG
                elif str(param_type).lower() == 'vlan':
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
                    raise self.database.DatabaseError(
                        Language.MSG_ERR_GENERIC.format(
                            self.utils.get_line(),
                            "There is no record found on table"))
            else:
                print Language.MSG_CMD_LIST_HELP
        except TypeError as exception:
            print exception.message
        except self.database.DatabaseError as exception:
            print exception.message

    def group(self, args):
        """
        Add device(s) or given type to group with params

        @param args:
        """
        device_id = None
        group_id = None
        try:
            if args:
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
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
                print Language.MSG_CMD_GROUP_HELP
        except TypeError as exception:
            print exception.message

    #this method works fine do not touch it!!!
    def show(self, args):
        """
        This method show running configuration by given option

        @param args:
        """
        try:
            #moderate type value to determine the statement
            if args:
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
                device_methods = DeviceMethods(params)
                config_methods = ConfigMethods(Config(), params)
                group_methods = GroupMethods()
                vlan_methods = VLanMethods()
                param_type = params.type.split()[0]
                # noinspection PyArgumentList
                if str(param_type).lower() == 'device':
                    # noinspection PyArgumentList
                    device_methods.show(params)
                elif str(param_type).lower() == 'group':
                    # noinspection PyArgumentList
                    group_methods.show(params)
                elif str(param_type).lower() == 'config':
                    # noinspection PyArgumentList
                    config_methods.show(params)
                elif str(param_type).lower() == 'vlan':
                    vlan_methods.show(params)
                else:
                    raise BaseException(
                        Language.MSG_ERR_GENERIC.format(
                            self.utils.get_line(),
                            'No [type] argument provided'
                        )
                    )
            else:
                print Language.MSG_CMD_SHOW_HELP
        except TypeError as exception:
            print exception.message

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
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
                device_methods = DeviceMethods(params)
                config_methods = ConfigMethods(Config(), params)
                group_methods = GroupMethods()
                vlan_methods = VLanMethods()
                param_type = params.type.split()[0]
                # noinspection PyArgumentList
                if str(param_type).lower() == 'device':
                    # noinspection PyArgumentList
                    params.command = "set"
                    device_methods.set(params)
                elif str(param_type).lower() == 'group':
                    # noinspection PyArgumentList
                    group_methods.set(params)
                elif str(param_type).lower() == 'config':
                    # noinspection PyArgumentList
                    config_methods.create(params)
                elif str(param_type).lower() == 'vlan':
                    vlan_methods.create(params)
                else:
                    raise TypeError(
                        Language.MSG_ERR_GENERIC.format(
                            self.utils.get_line(),
                            'No [type] argument provided'
                        )
                    )
            else:
                print Language.MSG_CMD_SET_HELP
        except TypeError as exception:
            print exception.message

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
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
                device_methods = DeviceMethods(params)
                group_methods = GroupMethods()
                param_type = params.type.split()[0]
                # noinspection PyArgumentList
                if str(param_type).lower() == 'device':
                    # noinspection PyArgumentList
                    params.command = "unset"
                    device_methods.set(params)
                elif str(param_type).lower() == 'group':
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
                print Language.MSG_CMD_UNSET_HELP
        except TypeError as exception:
            print exception.message

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
                arglist = self.utils.get_clean_params(args)
                params = self.argparser.get_args(arglist)
                param_type = params.type.split()[0]
                #set gathered id params to be used
                if params.id:
                    param_id = params.id.rstrip().lstrip()
                elif params.name:
                    param_name = params.name.rstrip().lstrip()
                else:
                    print Language.MSG_ERR_EMPTY_ID + \
                        '\n' + Language.MSG_ERR_EMPTY_NAME

                if param_type and param_id or param_name:
                    if str(param_type).lower() == 'group':
                        cmd = SQL.SQL_REMOVE_GROUP % {'id': int(param_id)}

                    #check if type is device to remove the group
                    # belong to given id and name
                    elif str(param_type).lower() == 'device':
                        cmd = SQL.SQL_REMOVE_DEVICE % {'id': int(param_id)}

                    #check if type is config to remove the group
                    # belong to given id and name
                    elif str(param_type).lower() == 'config':
                        cmd = SQL.SQL_REMOVE_CONFIG % {'id': int(param_id)}
                    #remove from given device from given group
                    elif str(param_type).lower() == 'from':
                        if params.group:
                            group_id = params.group.rstrip().lstrip()
                            cmd = SQL.SQL_REMOVE_DEVICE_FROM_GROUP % {
                                'device': int(param_id), 'group': int(group_id)}
                        else:
                            raise Exception(
                                Language.MSG_ERR_EMPTY_GROUP
                            )

                    #remove vlan record from database
                    elif str(param_type).lower() == 'vlan':
                        cmd = SQL.SQL_REMOVE_VLAN % {'id': int(param_id)}
                    else:
                        print Language.MSG_ERR_GENERIC.format(
                            self.utils.get_line(),
                            'No [type] argument provided')
            else:
                print Language.MSG_CMD_REMOVE_HELP

            if cmd:
                self.database.remove(cmd)
            else:
                raise RuntimeError("SQL command could not be created")
        except RuntimeError as exception:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(),
                                                  exception.message)

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
