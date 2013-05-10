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
from src.resources.Resources import Resources
from src.resources.SQL import SQL


__author__ = 'fatih'


class PostgreDriver(object):
    """
    PostgreDriver class implement a database interface between
    application database class and postgresql.

    Recently Database methods do all same thing such executing provided commands
    But they are all separated for future planning if it may be needed to
    implement detailed statements.
    """

    def __init__(self):
        """
        Constructor for Database class
        """
        self.__config__ = Resources.__db__config__
        self.__section__ = Resources.cfg_section_master_db
        self.utils = Utils()
        self.DatabaseError = db.DatabaseError
        self.config = ConfigParser.RawConfigParser()
        self.config.read(self.__config__)
        self.table_prefix = self.config.get(self.__section__, 'table_prefix')

    def connect(self):
        """
        Connect database with given parameters
        @return a live connection to keep transactions
        """

        try:

            #gather connection parameters from database config file
            db_name = self.config.get(self.__section__, 'db_name')
            user = self.config.get(self.__section__, 'username')
            password = self.config.get(self.__section__, 'password')
            host = self.config.get(self.__section__, 'host')
            conn_str = "dbname=" + db_name + " user=" + user + \
                       " password=" + password + " host=" + host
            conn = db.connect(conn_str)
            return conn
        except BaseException as exception:
            raise BaseException(
                Language.MSG_ERR_DATABASE_CONNECT % {exception.message}
            )

    def select(self, cmd):
        """
        Execute "SELECT" commands to retrieve rows from database.

        @param cmd is an SQL statement
        @return columns header and results
        """
        conn = None
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(cmd)
            fields = [i[0] for i in cur.description]
            results = cur.fetchall()
            conn.commit()
            #print Language.MSG_SUCCESS_SELECT
            return fields, results
        except BaseException:
            raise BaseException(
                Language.MSG_ERR_DATABASE_NORECORD
            )
        finally:
            self.close_conn(conn)

    def get(self, key, id, table_postfix="device"):
        """
        Execute "SELECT" commands to retrieve rows from database.

        @param key is an SQL statement
        @param id defines the primary key as id
        @param table_postfix is a value to determine the table with table prefix
        @return columns header and results
        """
        conn = None
        try:
            conn = self.connect()
            cur = conn.cursor()

            # generate table with table prefix and postfix
            table = self.table_prefix + "_" + table_postfix
            cmd = SQL.SQL_SELECT_BY_KEY % \
                  {
                      'key': key,
                      'table': table,
                      'id': id
                  }
            cur.execute(cmd)
            fields = [i[0] for i in cur.description]
            results = cur.fetchall()
            conn.commit()
            #print Language.MSG_SUCCESS_SELECT
            return fields, results
        except BaseException as exception:
            raise BaseException(
                Language.MSG_ERR_DATABASE_ERROR % {exception.message}
            )
        finally:
            self.close_conn(conn)

    def insert(self, cmd):
        """
        Execute "INSERT" SQL statements.

        Insert objects to database expected json formats for inserting objects.
        @param cmd is an SQL statement
        @return new record id
        """
        conn = None
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(cmd)
            rid = cur.fetchone()
            conn.commit()
            if rid:
                return rid
        except BaseException as exception:
            raise BaseException(
                Language.MSG_ERR_DATABASE_ERROR % {exception.message}
            )
        finally:
            self.close_conn(conn)

    def update(self, cmd):
        """
        Execute "UPDATE" SQL statements.

        Update database objects with given values

        @param cmd is an SQL statement
        @return True or False
        """
        conn = None
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(cmd)
            conn.commit()
            return True
        except BaseException as exception:
            raise BaseException(
                Language.MSG_ERR_DATABASE_ERROR % {exception.message}
            )
            return False
        finally:
            self.close_conn(conn)

    def remove(self, cmd):
        """
        Execute "DELETE" SQL statements.

        Remove records from database objects with given values

        @param cmd is an SQL statement
        """
        conn = None
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(cmd)
            conn.commit()
            print Language.MSG_SUCCESS_REMOVE
        except BaseException as exception:
            raise BaseException(
                Language.MSG_ERR_DATABASE_ERROR % {exception.message}
            )
        finally:
            self.close_conn(conn)

    @classmethod
    def close_conn(cls, con):
        """
        Close database live connection

        @param cls class itself
        @param con is initiated connection
        """
        try:
            if con:
                con.close()
        except cls.DatabaseError as exception:
            print Language.MSG_ERR_DATABASE_CLOSE.format(exception.message)




