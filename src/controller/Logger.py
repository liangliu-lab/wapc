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
import os
from src.model.Log import Log
from src.helpers.Utils import Utils
from src.database.Database import Database
from src.resources.Resources import Resources
import inspect


class Logger(logging.getLoggerClass()):
    """
    Logger class is an logging implementation uses CouchDB to record logs.

    Log types debug, info, warning, error and critical. Please see further
    details at
    http://docs.python.org/2/howto/logging.html#logging-basic-tutorial

    """

    def __init__(self, target=None):
        """
        Logger initializer
        @param target Database name
        @return:
        """
        self.utils = Utils()
        if not target:
            self.target = Resources.LOG_PATH % {'time': self.utils.day}
        else:
            self.target = target
        self.database = Database(self.utils.log_db, self.target)
        self.severity = Log.severity
        try:
            # try to connect log db server
            self.database.connect()

            # set type variable to decide what db will be used to log
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
        caller = inspect.stack()[1]
        # print caller[3]

        try:
            # write new log into log database
            if self.type == self.utils.log_db:
                log_id = self.database.insert(log)
                return log_id
            else:
                # send log into log file
                logger = logging.getLogger('debug-log')
                fh = logging.FileHandler(self.target)
                fh.setLevel(logging.DEBUG)
                logger.addHandler(fh)
                logger.log(log.get_severity(), log)
        except BaseException as exception:
            # If couchdb could not be connected all logs will be inserted into
            # local file system under /var/log till the new Logger instance will
            # be called.
            print "Error (%s) occurred on creating log method. " \
                  "Trying to fix..." % {exception.message}
            logger = logging.getLogger('debug-log')
            fh = logging.FileHandler(self.target)
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)
            logger.log(log.get_severity(), log)


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

    def tail(self, f, lines=1, _buffer=1024):

        """Tail a file and get X lines from the end"""
        # place holder for the lines found
        lines_found = []

        # block counter will be multiplied by buffer
        # to get the block size from the end
        block_counter = -1

        # loop until we find X lines
        while len(lines_found) < lines:
            try:
                f.seek(block_counter * _buffer, os.SEEK_END)
            except IOError:  # either file is too small, or too many lines requested
                f.seek(0)
                lines_found = f.readlines()
                break

            lines_found = f.readlines()

            # we found enough lines, get out
            if len(lines_found) > lines:
                break

            # decrement the block counter to get the
            # next X bytes
            block_counter -= 1

        return lines_found[-lines:]

"""
def try_log():
    my_logger = Logger()
    log_id = my_logger.create_log(
        'Test Log',
        Log.severity.DEBUG,
        my_logger.utils.get_line(),
        'Logger test message',
        'create_log',
        'facility',
        'localhost')
    print "New log created with id: " + log_id

    print my_logger.gather_logs(None, '_all_docs')

if __name__ == "__main__":
    #mylogger.tail("/var/log/labris/")
    try_log()
"""

