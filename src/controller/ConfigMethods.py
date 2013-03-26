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

@package controller
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

"""
import json
import os
import threading
from time import strftime, gmtime
from src.cli.CommunicationInterface import CommunicationInterface
from src.model.Device import Device
from src.resources.SQL import SQL
from src.controller.DeviceMethods import DeviceMethods
from src.database.Database import Database
from src.helper.Utils import Utils
from src.language.Language import Language
from src.resources.Resources import Resources
from src.model.Config import Config


class ConfigMethods(threading.Thread):
    """
    ConfigMethods class aims to provide required metdhos to requester class
    or methods to read, update Config object.
    """

    def __init__(self, new_config, params):
        """
        Constructer of ConfigMethods

        @param new_config Is a new config tuple object to update self.config
        @param params Is used to set new parameters to recent instance
        """
        super(ConfigMethods, self).__init__()
        self.utils = Utils()
        self.database = Database()
        self.communication_interface = CommunicationInterface()
        self.script = Resources.ci_script
        self.cfg_device = Resources.cfg_device_resource
        self.now = strftime(Resources.time_format, gmtime())

        self.config = Config()
        self.set_config(new_config)

        self.params = None
        self.set_params(params)

    def create(self, params):
        """
        This method is used to create a config independently
        :param params:
        """
        config = Config()
        device = Device()

        try:
            #===================================
            # check namespace variables if set then set
            # them into device model variables
            #===================================

            # set device ip to connect to the device
            if params.ip:
                device.set_ip(params.ip.strip())
            else:
                print Language.MSG_ERR_EMPTY_IP.format('device')
                device.set_ip(raw_input("Please enter an IP address:"))

            # set device name to connect to the device
            if params.name:
                device.set_name(params.name.strip())
            else:
                print Language.MSG_ERR_EMPTY_NAME.format('device')
                device.set_name(raw_input("Please enter an nick name:"))

            # set device description to connect to the device
            if params.description:
                device.set_description(params.description.strip())
            else:
                print Language.MSG_ERR_EMPTY_DESC.format('device')

            # set device username to connect to the device
            if params.username:
                device.set_username(params.username.strip())
            else:
                print Language.MSG_ERR_EMPTY_USERNAME.format('device')
                device.set_username(raw_input("Please enter an username:"))

            # set device password to connect to the device
            if params.password:
                device.set_password(params.password.strip())
            else:
                print Language.MSG_ERR_EMPTY_PASSWORD.format('device')
                device.set_password(raw_input("Please enter a password:"))

            #set config parameters to relate with device
            config.set_name(device.get_name())
            config.set_username(device.get_username())
            config.set_password(device.get_password())
            config.set_ip(device.get_ip())
            config.set_enable_password(config.get_password())
            config.set_transport_protocol(
                device.get_config().get_transport_protocol())
            config.set_personality(device.get_config().get_personality())

            #check if rpc is responded

            cmd = SQL.SQL_INSERT_CONFIG % {
                "name": config.get_name(),
                "description": config.get_description(),
                "ip": config.get_ip(),
                "radius_config_id": config.get_radius(),
                "ssid": config.get_ssid(),
                "vlan_id": config.get_vlan(),
                "channel": config.get_channel(),
                "maxclients": config.get_maxclient(),
                "username": config.get_username(),
                "password": config.get_password(),
                "enable_password": config.get_enable_password(),
                "transport_protocol": config.get_transport_protocol(),
                "personality": config.get_personality(),
                "date_added": self.now,
                "date_modified": self.now
            }
        except RuntimeError as exception:
            print exception.message

    def read(self, config_id):
        """

        :param config_id:
        """
        try:
            #check namespace variables if set

            #moderate type value to determine the statement
            cmd = SQL.SQL_SELECT_CONFIG_DETAIL % {'id': int(config_id)}
            fields, results = self.database.select(cmd)
            if fields and results:
                rset = {"fields": fields,
                        "results": [list(f) for f in results][0]}
                return rset
            else:
                raise Exception(
                    Language.MSG_ERR_GENERIC.format(
                        self.utils.get_line(),
                        "There is no config record found on table"))
        except ValueError as exception:
            print exception.message

    def set(self, config):
        """
        Set method will update given config by parameter
        @param config is a Config model which provided by parameter
        """

    def update(self, params):
        """
        Update methods certainly moderated by $ edit [OPTIONS] command by CLI.
        This methods only inherit update database
        records by no touching physical device config.

        @param params
        """
        cmd = None
        config = Config()
        try:
            if params.id:
                did = params.id.strip()
            else:
                print Language.MSG_ADD_ID_HELP
                did = raw_input("Please enter 'id' value:").strip()

            if params.option:
                option = params.option.strip()
            else:
                print Language.MSG_ADD_OPTION_HELP
                option = raw_input("Please enter 'option' value:").strip()

            if params.param:
                param = params.param.strip()
            else:
                print Language.MSG_ADD_PARAM_HELP
                param = raw_input("Please enter 'param' value:").strip()

            if did and option and param:
                if option in config:
                    cmd = SQL.SQL_UPDATE_DEVICE_CONFIG % \
                          {
                              "key": option,
                              "value": param,
                              "modified": self.now,
                              "id": int(did)
                          }

                if self.database.update(cmd):
                    print Language.MSG_UPDATE_RECORD.format(
                        'device', did, config.get_name())
                else:
                    print Language.MSG_ERR_DATABASE_ERROR.format(
                        self.utils.get_line(), 'updating recorded group', did)
            else:
                raise Exception(
                    "Error occured while getting required parameters "
                    "device 'id', option, and param")
        except BufferError as exception:
            print exception.message

    def run(self):
        """
        This methods runs a thread to update pyshical devices by
        given parameters gathered from database
        """
        while True:
            try:
                device_methods = DeviceMethods(self.get_config())
                if device_methods.group_set(
                        self.get_config(), self.get_params()
                ):
                    break
            except RuntimeError as exception:
                print exception.message
                break

    def delete(self, params):
        """

        :param params:
        """

    def show(self, params):
        """

        :param params:
        """

    def set_config(self, config):
        """
        ConfigMethods controller class config setter
        @param config is a Config object includes details
        """
        self.config.update(config)

    def get_config(self):
        """
        ConfigMethods controller class config getter
        @return config is a Config object
        """
        return self.config

    def set_params(self, params):
        """
        ConfigMethods controller class config setter
        @param params is a Config object includes details
        """
        self.params = params

    def get_params(self):
        """
        ConfigMethods controller class config getter
        @return params is a Config object
        """
        return self.params