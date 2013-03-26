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


class VLan(object):
    """
        VLan object
    """

    def __init__(self):
        """
        Constructer for VLan model
        """
        self.name = None
        self.inet = None
        self.subnet = None
        self.number = None
        self.interface = None

    def set_name(self, name):
        """
        Setter for name variable of VLan
        @param name
        """
        self.name = name

    def get_name(self):
        """
        Getter for name variable of VLan
        @return VLan configuration name
        """
        return self.name

    def set_ip(self, inet):
        """
        Setter for IP variable of VLan
        @param inet
        """
        self.inet = inet

    def get_ip(self):
        """
        Getter for IP variable of VLan
        @return VLan ip
        """
        return self.inet

    def set_subnet(self, subnet):
        """
        Setter for subnet variable of VLan

        @param subnet
        """
        self.subnet = subnet

    def get_subnet(self):
        """
        Getter for subnet

        @return subnet
        """
        return self.subnet

    def set_number(self, number):
        """
        Setter for number variable
        @param number
        """
        self.number = number

    def get_number(self):
        """
        Getter for number

        @return number
        """
        return self.number

    def set_interface(self, interface):
        """
        Setter for interface

        @param interface
        """
        self.interface = interface

    def get_interface(self):
        """
        Getter for interface such eth0, eth1

        @return recent instance interface
        """
        return self.interface