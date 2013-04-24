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

@package model
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

"""

from src.model.Config import Config


class Device(Config):
    """
        Device object class to create a runtime
        instance while adding a new device

        Each device has its own configuration values provided by user via CLI
        and its configuration is kept on a path defined like:
        brand/model/firmware under root config path.

        @implements Config
    """

    def __init__(self):
        """
        Constructor for Device model
        """
        super(Device, self).__init__()
        self["id"] = None
        self["ip"] = None
        self["brand"] = 'cisco'
        self["model"] = 'cisco'
        self["firmware"] = 'cisco'
        self["relation"] = 'slave'
        self["config_id"] = None
        self["config"] = Config()

    def set_id(self, d_id):
        """
        Setter for id variable is a private method

        @param d_id int gathered from database
        """
        self["id"] = d_id

    def get_id(self):
        """
        Getter for instance device ipcut

        @return d_ip as device ip
        """
        return self["id"]

    def set_ip(self, d_ip):
        """
        Setter for id variable is a private method

        @param d_ip int gathered from database
        """
        self["ip"] = d_ip

    def get_ip(self):
        """
        Getter for instance device id

        @return d_ip as device id
        """
        return self["ip"]

    def set_device_brand(self, brand):
        """
        Setter for brand variable

        Brand parameter is a required parameter. It has to be provided by user
        and also required configuration .conf file should be under well-formed
        folder structure to gather configuration file when adding a new device
        into inventory. Otherwise no configuration will be loaded to the device.

        If brand parameter is provided but model or firmware parameters not then
        user or system administrator should create path as below:
        brand/default/default

        The software will look the given path if it is provided otherwise it
        assumes default path already exists.

        @param brand string Variable defines such as Cisco, 3comm, etc.
        """
        self["brand"] = brand

    def get_brand(self):
        """
        Getter for brand variable
        @return brand variable
        """
        return self["brand"]

    def set_model(self, model):
        """
        Setter for model variable
        @param model string Regarding provided brand
        """
        self["model"] = model

    def get_model(self):
        """
        Getter for model
        @return model
        """
        return self["model"]

    def set_firmware(self, firmware):
        """
        Setter for Device firmware variable
        @param firmware string
        """
        self["firmware"] = firmware

    def get_firmware(self):
        """
        Getter for firmware
        @return instance firmware
        """
        return self["firmware"]

    def set_relation(self, relation):
        """
        Setter for relation variable.

        Relation variable is important to define what relation exists between
        devices in inventory either Master or Slave. Devices configure
        themselves to work in a master/slave topology therefore this variable
        has to bet. Otherwise the application will assume the device recently
        been adding is a slave. There has to be one master to work devices
        effectively.

        @param relation string master or slave
        """
        self["relation"] = relation

    def get_relation(self):
        """
        Getter for relation variable
        @return instance relation
        """
        return self["relation"]

    def set_name(self, name):
        """
        Setter for name parameter

        Name parameter is a variable to define a nickname for device(s). It
        should be unique.

        @param name string Nickname for device as unique
        """
        self["name"] = name

    def get_name(self):
        """
        Getter for name variable

        @return instance name
        """
        return self["name"]

    def set_description(self, description):
        """
        Setter for description variable to describe device in detail.

        @param description text Description
        """
        self["description"] = description

    def get_description(self):
        """
        Getter for description

        @return instance description
        """
        return self["description"]

    def set_config_id(self, config_id):
        """
        Setter for config_id

        @param config_id int Config model instance id at runtime
        """
        self["config_id"] = config_id

    def get_config_id(self):
        """

        @return instance configuration id
        """
        return self["config_id"]

    def set_config(self, config):
        """
        Setter to set a Config model into device instance config

        @param config dict is a Config model as a dictionary object
        """
        self["config"] = config

    def get_config(self):
        """
        Getter for Device model to get instance Config

        @return Config model
        """
        return self["config"]