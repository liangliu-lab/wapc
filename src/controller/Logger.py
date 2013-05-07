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
import time
from src.model.Log import Log
from src.helpers.Utils import Utils
from src.database.Database import Database
from src.resources.Resources import Resources


class Logger(logging.getLoggerClass()):
    """
    Logger class is an logging implementation uses CouchDB to record logs.

    Log types debug, info, warning, error and critical. Please see further
    details at
    http://docs.python.org/2/howto/logging.html#logging-basic-tutorial

    """

    def __init__(self):
        """
        Logger initializer
        @return:
        """
        self.utils = Utils()
        self.database = Database(self.utils.log_db)
        self.severity = Log.severity
        try:
            # try to connect log db server
            self.database.connect()
            self.type = self.utils.log_db
        except BaseException:
            print "WARNING:\tLog server could not be reached. " \
                  "System logs will be use as default."
            self.type = "logging"

    def create_log(self, name, severity, line, message, method,
                   facility, host):
        """
        Create Log by given parameters

        @param name
        @param severity
        @param line
        @param message
        @param method
        @param facility
        @param host
        @return log id gathered from log database
        """
        log = Log(name, severity, line, message, method, facility,
                  host)
        try:
            # write new log into log database
            if self.type == self.utils.log_db:
                log_id = self.database.insert(log)
                return log_id
            else:
                # send log into log file
                logger = logging.getLogger('debug-log')
                fh = logging.FileHandler(
                    Resources.LOG_PATH % {'time': self.utils.day}
                )
                fh.setLevel(logging.DEBUG)
                logger.addHandler(fh)
                logger.error(log)
        except BaseException as exception:
            print "Error (%s) occurred on creating log method. " \
                  "Trying to fix..." % {exception.message}
            time.sleep(5000)
            self.database.connect()

    def gather_logs(self, params, opt='_all_docs'):
        """
        Gather logs by given params
        @param params to create query by given dict objects
        @param opt to define which log documents will be gathered
        @return:
        """
        try:
            if opt == '_all_docs':
                cmd = opt
            else:
                cmd = params
            fields, results = self.database.select(cmd)
            return self.utils.formatter(fields, results)
        except BaseException as exception:
            print exception.message

    def delete_logs(self, params, opt='_all_docs'):
        """
        Delete log docs by given params
        @param params to create query by given dict objects
        @param opt to define which log documents will be gathered
        @return:
        """
        try:
            if opt == '_all_docs':
                cmd = opt
            else:
                cmd = params
            fields, results = self.database.remove(cmd)
            return self.utils.formatter(fields, results)
        except BaseException as exception:
            print exception.message
