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

@package cli
@date 4/26/13
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Teknoloji

"""
from time import strftime, gmtime
from src.resources.Resources import Resources
from argparse import Namespace

__author__ = 'fatih'


class Log(dict):
    """
    Log class is used to define log model data structure and
    """
    severity = Namespace()
    severity.CRITICAL = 'CRITICAL'
    severity.DEBUG = 'DEBUG'
    severity.ERROR = 'ERROR'
    severity.WARNING = 'WARNING'
    severity.FATAL = 'FATAL'
    severity.INFO = 'INFO'

    def __init__(self,
                 name="Default Log",
                 severity=str(severity.INFO),
                 line=None,
                 message="Log Message",
                 method="Method name",
                 facility="Default Facility",
                 host="192.168.0.1"):
        """
        Constructor for Log model
        @return:
        """
        super(Log, self).__init__()
        self.now = strftime(Resources.time_format, gmtime())
        self["timestamp"] = self.now
        self["name"] = name
        self["severity"] = str(severity)         # set default severity info
        self["line"] = line
        self["message"] = message
        self["method"] = method
        self["facility"] = facility
        self["host"] = host

    def set_timestamp(self, timestamp):
        """
        Setter for timestamp
        @param timestamp
        """
        self["timestamp"] = timestamp

    def get_timestamp(self):
        """
        Getter for timestamp
        @return timestamp
        """
        return self["timestamp"]

    def set_name(self, name):
        """
        Setter for name
        @param name
        """
        self["name"] = name

    def get_name(self):
        """
        Getter for name
        @return name
        """
        return self["name"]

    def set_severity(self, severity):
        """
        Setter for severity
        @param severity
        """
        self["severity"] = severity

    def get_severity(self):
        """
        Getter for severity
        @return severity
        """
        return self["severity"]

    def set_line(self, line):
        """
        Setter for line
        @param line
        """
        self["line"] = line

    def get_line(self):
        """
        Getter for line
        @return line
        """
        return self["line"]

    def set_message(self, message):
        """
        Setter for message
        @param message
        """
        self["message"] = message

    def get_message(self):
        """
        Getter for message
        @return message
        """
        return self["message"]

    def set_method(self, method):
        """
        Setter for method
        @param method
        """
        self["method"] = method

    def get_method(self):
        """
        Getter for message
        @return message
        """
        return self["method"]

    def set_facility(self, facility):
        """
        Setter for facility
        @param facility
        """
        self["facility"] = facility

    def get_facility(self):
        """
        Getter for facility
        @return facility
        """
        return self["facility"]

    def set_host(self, host):
        """
        Setter for host
        @param host
        """
        self["host"] = host

    def get_host(self):
        """
        Getter for host
        @return host
        """
        return self["host"]










