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
import psycopg2 as db
from src.helpers.Utils import Utils
from src.language.Language import Language
from PostgreDriver import PostgreDriver
from CouchDriver import CouchDriver
from src.resources.Resources import Resources
from src.resources.SQL import SQL


__author__ = 'fatih'


class Database(object):
    """
    Database class implement a database interface between
    application and postgresql.

    Recently Database methods do all same thing such executing provided commands
    But they are all separated for future planning if it may be needed to
    implement detailed statements.
    """

    def __init__(self, type):
        """
        Constructor for Database class
        """
        self.__db_config__ = Resources.__db__config__
        self.__system_config__ = Resources.__config__system__
        self.__system_section__ = Resources.cfg_section_system
        self.__section__ = Resources.cfg_section_master_db
        self.utils = Utils()
        self.DatabaseError = db.DatabaseError

        # gather overall system configurations
        self.config = ConfigParser.RawConfigParser()
        self.config.read(self.__system_config__)

        # gather overall database configurations
        self.db_config = ConfigParser.RawConfigParser()
        self.db_config.read(self.__db_config__)
        self.table_prefix = self.db_config.get(self.__section__, 'table_prefix')

        # retrieve provided database type which defines what db will be used
        # with this instance
        self.type = type
        self.master_driver = PostgreDriver()
        self.log_db_driver = CouchDriver()

    def connect(self):
        """
        Connect database with given parameters
        @return a live connection to keep transactions
        """

        try:

            #gather connection parameters from database config file
            if self.type == self.config.get(
                    self.__system_section__, "master_db"):
                self.master_driver.connect()
            elif self.type == self.config.get(
                    self.__system_section__, "log_db"):
                self.log_db_driver.connect()
            return True
        except BaseException as exception:
            raise Language.MSG_ERR_DATABASE_CONNECT.format(exception.message)

    def select(self, cmd):
        """
        Execute "SELECT" commands to retrieve rows from database.

        @param cmd is an SQL statement
        @return columns header and results
        """
        try:
            if self.type == self.config.get(
                    self.__system_section__, "master_db"):
                fields, results = self.master_driver.select(cmd)
            elif self.type == self.config.get(
                    self.__system_section__, "log_db"):
                fields, results = self.log_db_driver.select(cmd)
            return fields, results
        except BaseException as exception:
            raise BaseException(
                exception.message
            )

    def get(self, key, id, table_postfix="device"):
        """
        Execute "SELECT" commands to retrieve rows from database.

        @param key is an SQL statement
        @param id defines the primary key as id
        @param table_postfix is a value to determine the table with table prefix
        @return columns header and results
        """
        try:
            if self.type == self.config.get(self.__system_section__,
                                            "master_db"):
                result = self.master_driver.get(key, id,
                                                            table_postfix)
            elif self.type == self.config.get(self.__system_section__,
                                              "log_db"):
                result = self.log_db_driver.get(key, id,
                                                            table_postfix)
            return result
        except BaseException as exception:
            raise BaseException(
                exception.message
            )

    def insert(self, cmd):
        """
        Execute "INSERT" SQL statements.

        Insert objects to database expected json formats for inserting objects.
        @param cmd is an SQL statement
        @return new record id
        """
        rid = None
        try:
            if self.type == self.config.get(
                    self.__system_section__, "master_db"):
                rid = self.master_driver.insert(cmd)
            elif self.type == self.config.get(
                    self.__system_section__, "log_db"):
                rid = self.log_db_driver.insert(cmd)
            if rid:
                return rid
        except BaseException as exception:
            raise BaseException(
                exception.message
            )

    def update(self, cmd):
        """
        Execute "UPDATE" SQL statements.

        Update database objects with given values

        @param cmd is an SQL statement
        @return True or False
        """
        try:
            if self.type == self.config.get(
                    self.__system_section__, "master_db"):
                self.master_driver.update(cmd)
            elif self.type == self.config.get(
                    self.__system_section__, "log_db"):
                self.log_db_driver.update(cmd)
            return True
        except BaseException:
            raise BaseException(
                Language.MSG_ERR_DATABASE_UPDATE
            )

    def remove(self, cmd):
        """
        Execute "DELETE" SQL statements.

        Remove records from database objects with given values

        @param cmd is an SQL statement
        """
        try:
            if self.type == self.config.get(
                    self.__system_section__, "master_db"):
                self.master_driver.remove(cmd)
            elif self.type == self.config.get(
                    self.__system_section__, "log_db"):
                self.log_db_driver.remove(cmd)
        except BaseException as exception:
            raise BaseException(
                Language.MSG_ERR_DATABASE_ERROR % {exception.message}
            )




