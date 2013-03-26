# coding=utf-8
"""
Copyright 2013 Labris Technology.

Licensed under the Apache License, Version 2.0 (the "License"):;
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http//www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@package model
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

"""

from src.model.Request import Request


class Config(dict):
    """
    Device configuration model to implement new instance while
    inserting a new device

    @implements dict object
    """

    def __init__(self):
        """
        Constructer for Config model
        """
        super(Config, self).__init__()
        self["id"] = None
        self["name"] = 'Default Device'
        self["description"] = 'Default desc for device'
        self["ip"] = "10.6.1.200"
        self["username"] = 'Cisco'
        self["password"] = 'Cisco'
        self["enable_password"] = 'Cisco'
        self["radius_config_id"] = 0
        self["transport_protocol"] = 'Telnet'
        self["personality"] = 'ios'
        self["ssid"] = "LBREAP"
        self["vlan_id"] = 0
        self["channel"] = 10
        self["maxclient"] = 20
        self["request"] = Request()
        self["Add Date"] = None
        self["Last Modified"] = None

    def __set_id(self, c_id):
        """
        Setter for id variable

        __set_id is a private method to set recent instance id gathered from
        database.

        @param c_id instance record id
        """
        self["id"] = c_id

    def __get_id(self):
        """
        Getter for instance id
        @return id instance id
        """
        return self["id"]

    def set_name(self, name):
        """
        Setter for name variable

        @param name string
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
        Setter for Config description

        A description for recent Config to describe the Config in detail
        @param description text
        """
        self["description"] = description

    def get_description(self):
        """
        Getter for description

        @return instance description
        """
        return self["description"]

    def set_ip(self, inet):
        """
        Setter for ip

        @param inet
        """
        self["ip"] = inet

    def get_ip(self):
        """
        Getter for ip variable
        return
        """
        return self["ip"]

    def set_username(self, username):
        """
        This username variable is set to define connection parameters for given
        device.

        @param username
        """
        self["username"] = username

    def get_username(self):
        """
        @return instance username
        """
        return self["username"]

    def set_password(self, password):
        """
        This password variable is set to define connection parameters for given
        device.
        
        @param password
        """
        self["password"] = password

    def get_password(self):
        """
        @return instance password
        """
        return self["password"]
    
    def set_enable_password(self, option):
        """
        This variable is set to define enable connection parameters for given
        device. In order to provide this variable users will be let to get the
        device in enable mode and make configuration changes.
        
        @param option as a enable password
        """
        self["enable_password"] = option

    def get_enable_password(self):
        """
        Getter for enable password variable

        @return enable password
        """
        return self["enable_password"]

    def set_radius(self, radius_config_id):
        """
        Setter for radius configuration id for recent Config instance

        @param radius_config_id radius server ip
        """
        self["radius_config_id"] = radius_config_id

    def get_radius(self):
        """
        Get radius variable
        @return radius server ip
        """
        return self["radius_config_id"]

    def set_ssid(self, ssid):
        """
        Setter for ssid variable

        @param ssid for recent config ssid
        """
        self["ssid"] = ssid

    def get_ssid(self):
        """
        Getter for ssid
        @return recent instance ssid
        """
        return self["ssid"]

    def set_vlan(self, vlan_id):
        """
        Setter for vlan variable
        @param vlan_id
        """
        self["vlan_id"] = vlan_id

    def get_vlan(self):
        """
        Getter for vlan
        @return vlan
        """
        return self["vlan_id"]

    def set_channel(self, channel):
        """
        Setter for channel
        @param channel
        """
        self["channel"] = channel

    def get_channel(self):
        """
        Getter for channel variables
        @return channel
        """
        return self["channel"]

    def set_transport_protocol(self, protocol):
        """
        Setter for transport protocol
        @param protocol
        """
        self["transport_protocol"] = protocol

    def get_transport_protocol(self):
        """
        Getter for transport protocol

        @return transport protocol
        """
        return self["transport_protocol"]

    def set_personality(self, personality):
        """
        Setter for personality

        Personality variable defined to implement personality while connecting
        a device.
        @param personality
        """
        self["personality"] = personality

    def get_personality(self):
        """
        Getter for personality

        @return personality as a string
        """
        return self["personality"]

    def set_maxclient(self, request):
        """
        Setter for maxclient

        Maxclient variables aims to define how many client can connect to the
        device as concurrent.
        @param request
        """
        self["maxclient"].update(request)

    def get_maxclient(self):
        """
        Getter for maxclient variable

        @return recent instance maxclient
        """
        return self["maxclient"]

    def set_request(self, request):
        """
        Set request

        @param request
        """
        self["request"].update(request)

    def get_request(self):
        """
        Getter for Request model
        @return Request model as a child instance of Config
        """
        return self["request"]

    def set_date_add(self, date):
        """
        Set add date of recent Config instance

        @param date
        """
        self["Add Date"] = date

    def get_date_add(self):
        """
        Add date of Config instance
        @return date the configuration added into database
        """
        return self["Add Date"]

    def set_date_modified(self, date):
        """
        Set last modified date for recent instance
        @param date
        """
        self["Last Modified"] = date

    def get_date_modified(self):
        """

        @return last modified date
        """
        return self["Last Modified"]