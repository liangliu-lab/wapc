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

@package database
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

"""
import ConfigParser
import couchdb
from src.helpers.Utils import Utils
from src.language.Language import Language
from src.resources.Resources import Resources


__author__ = 'fatih'


class CouchDriver(object):
    """
    CouchDriver class implement a database interface between
    application database class and CouchDB.

    Recently Database methods do all same thing such executing provided commands
    But they are all separated for future planning if it may be needed to
    implement detailed statements.
    """

    def __init__(self):
        """
        Constructor for CouchDriver class
        """
        self.__config__ = Resources.__db__config__
        self.__section__ = Resources.cfg_section_log_db
        self.utils = Utils()
        self.DatabaseError = Exception("Error occurred on CouchDB operations")
        self.config = ConfigParser.RawConfigParser()
        self.config.read(self.__config__)
        self.server_location = self.config.get(self.__section__, 'host')
        self.db_name = self.config.get(self.__section__, 'db_name')
        self.db_username = self.config.get(self.__section__, 'username')
        self.db_password = self.config.get(self.__section__, 'password')
        self.database = None

    def connect(self):
        """
        Connect database with given parameters
        @return a live connection to keep transactions
        """

        try:
            #gather connection parameters from database config file
            server = couchdb.Server(self.server_location)
            server.resource.credentials = (self.db_username, self.db_password)
            # check if log database exists otherwise create one
            try:
                self.database = server[self.db_name]
            except BaseException:
                server.create(self.db_name)
                self.database = server[self.db_name]
        except BaseException as exception:
            raise BaseException(
                Language.MSG_ERR_LOG_SERVER_CONNECTION %
                {
                    'command': 'connecting',
                    'exception': exception.message
                }
            )

    def select(self, cmd):
        """
        Execute "SELECT" commands to retrieve rows from database.

        @param cmd is an Nosql statement
        @return columns header and results
        """
        try:
            rows = self.database.view(cmd)
            fields = ['name', 'facility', 'timestamp', 'log revision',
                      'line number', 'host', 'long message', 'log id',
                      'method name', 'method']
            results = []
            for row in rows:
                results.append(
                    [v for k, v in dict(self.database[row.id]).items()]
                )
            return fields, results
        except self.DatabaseError as exception:
            raise BaseException(
                Language.MSG_ERR_LOG_SERVER_CONNECTION %
                {
                    'command': "selecting database",
                    'exception': exception.message
                }
            )

    def insert(self, doc):
        """
        Execute "INSERT" Nosql statements.

        Insert objects to database expected json formats for inserting objects.
        @param doc is a couchdb document
        @return new record id
        """
        try:
            rid, rev = self.database.save(doc)
            self.database.commit()
            if rid:
                return rid
        except BaseException as exception:
            raise BaseException(
                Language.MSG_ERR_DATABASE_ERROR.format(
                    self.utils.get_line(), 'inserting', exception.message)
            )

    def update(self, cmd):
        """
        Execute "UPDATE" Nosql statements.

        Update database objects with given values

        @param cmd is an Nosql statement
        @return True or False
        """
        try:
            self.database.update(cmd)
            self.database.commit()
            return True
        except BaseException as exception:
            raise BaseException(
                Language.MSG_ERR_DATABASE_ERROR.format(
                    self.utils.get_line(), 'updating', exception.message)
            )

    def remove(self, doc):
        """
        Execute "DELETE" SQL statements.

        Remove records from database objects with given values

        @param doc is a Couchdb document
        """
        try:
            self.database.delete(doc)
            self.database.commit()
            print Language.MSG_SUCCESS_REMOVE
        except BaseException as exception:
            raise BaseException(
                Language.MSG_ERR_DATABASE_ERROR.format(
                    self.utils.get_line(), 'removing', exception.message)
            )




