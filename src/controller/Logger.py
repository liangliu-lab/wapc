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

import logging
from src.model.Log import Log
from src.helpers.Utils import Utils
from src.database import Database


class Logger(logging):
    """
    Logger class is an logging implementation uses CouchDB to record logs.

    Log types debug, info, warning, error and critical. Please see further
    details at
    http://docs.python.org/2/howto/logging.html#logging-basic-tutorial

    """

    def __init__(self, ):
        """
        Logger initializer
        @return:
        """
        self.utils = Utils()
        self.database = Database(self.utils.logdb)

    def create_log(self, timestamp, name, severity, line, message, method,
                   facility, host):
        """
        Create Log by given parameters
        @param timestamp is a Log model to handle log data and its own variables
        @param name
        @param severity
        @param line
        @param message
        @param method
        @param facility
        @param host
        @return log id gathered from log database
        """
        log = Log(timestamp, name, severity, line, message, method, facility,
                  host)
        try:
            self.database.insert(log)

        except:
            pass
