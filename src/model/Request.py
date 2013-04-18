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
from src.model.Commands import Commands


class Request(dict):
    """
        Request object class to generate a new request
        "enable":true,
        "configure":false,
        "commands":[
            {
                "command":"showa dot11 bssid"
            }
        ]
    """
    def __init__(self):
        """
        Constructor for Request model
        """
        super(Request, self).__init__()
        self["enable"] = True
        self["configure"] = False
        self["commands"] = Commands()

    def set_enable(self, status):
        """
        Setter for enable variable

        Enable variable required by devices to enable configuration mode true
        or false and then device decides to let the user make configuration(s)
        on the device.

        @param status true or false
        """
        self["enable"] = status

    def get_enable(self):
        """
        Getter for enable variable

        @return enable true or false
        """
        return self["enable"]

    def set_configure(self, status):
        """
        Setter for configure variable

        Configure variable required by devices to let the user make
        configuration(s) on the device.

        @param status true or false
        """
        self["configure"] = status

    def get_configure(self):
        """
        Getter for configure variable

        @return configure true or false
        """
        return self["configure"]

    def set_commands(self, commands):
        """
        Setter for commands

        This method set Commands model provided by other methods to Request
        object

        @param commands Commands model
        """
        self["commands"] = commands

    def get_commands(self):
        """
        Getter for Commands

        @return instance Commands model
        """
        return self["commands"]