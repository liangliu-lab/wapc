"""
This file will be used to implement database interactions with postgresql

"""
from Queue import Empty
import datetime
import psycopg2 as db
import ConfigParser
import sys
from src.language.language import Language
from src.resources.resources import Resources

__author__ = 'fatih'

class Database:
    """
        Database class implement a database interface between application and postgresql
    """
    __config__ = Resources.__db__config__
    __section__ = Resources.cfg_section_postgre

    def connect(self):
        """
            Connect database with given parameters
        """
        try:
            config = ConfigParser.RawConfigParser()
            config.read(self.__config__)
            #gather connection parameters from database config file
            dt = datetime.datetime.now()
            db_name = config.get(self.__section__, 'db_name')
            user = config.get(self.__section__, 'username')
            password = config.get(self.__section__, 'password')
            host = config.get(self.__section__, 'host')
            connStr = "dbname=" + db_name + " user=" + user + " password=" + password + " host=" + host
            conn = db.connect(connStr)
            return conn
        except db.DatabaseError as e:
            print Language.MSG_ERR_DATABASE_ERROR.format('35','connecting',e.message)
            pass
        except ConfigParser.NoSectionError as e:
            print Language.MSG_ERR_NO_CONFIG_SECTION.format(e.messagem)
            pass
        except IOError as e:
            print Language.MSG_ERR_IO_ERROR.format(e.errno, e.strerror)
            pass
        except Exception as e:
            print Language.MSG_ERR_DB_CONNECT.format(e.message)
            pass

    def select(self, cmd):
        """
            Remove objects from given tables
        """
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(cmd)
            results = cur.fetchall()
            conn.commit()
            print Language.MSG_SUCCESS_SELECT
            self.close_conn(conn)
            return results
        except db.DatabaseError as e:
            print Language.MSG_ERR_DATABASE_ERROR.format('63','selecting',e.message)
            pass
        except IOError as e:
            print Language.MSG_ERR_IO_ERROR.format(e.errno, e.strerror)
            pass
        except Exception as e:
            print Language.MSG_ERR_DB_CONNECT.format(e.message)
            pass

    def insert(self, cmd):
        """
            Insert objects to database
            expected json formats for inserting objects
        """
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(cmd)
            id = cur.fetchone()
            conn.commit()
            if id is Empty:
                pass
            else:
                return id
            self.close_conn(conn)
        except db.DatabaseError as e:
            print Language.MSG_ERR_DATABASE_ERROR.format('76','inserting',e.message)
            pass
        except IOError as e:
            print Language.MSG_ERR_IO_ERROR.format(e.errno, e.strerror)
            pass
        except Exception as e:
            print Language.MSG_ERR_DB_CONNECT.format(e.message)
            pass

    def update(self, cmd):
        """
            Update database objects with given values
        """
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(cmd)
            conn.commit()
            self.close_conn(conn)
        except db.DatabaseError as e:
            print Language.MSG_ERR_DATABASE_ERROR.format('90','updating',e.message)
            pass
        except IOError as e:
            print Language.MSG_ERR_IO_ERROR.format(e.errno, e.strerror)
            pass
        except Exception as e:
            print Language.MSG_ERR_DB_CONNECT.format(e.message)
            pass

    def remove(self, cmd):
        """
            Remove objects from given tables
        """
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(cmd)
            conn.commit()
            print Language.MSG_SUCCESS_REMOVE
            self.close_conn(conn)
        except db.DatabaseError as e:
            print Language.MSG_ERR_DATABASE_ERROR.format('90','updating',e.message)
            pass
        except IOError as e:
            print Language.MSG_ERR_IO_ERROR.format(e.errno, e.strerror)
            pass
        except Exception as e:
            print Language.MSG_ERR_DB_CONNECT.format(e.message)
            pass

    def get_last_insertID(self):
        """

        """
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("SELECT lastval() from apc_device")
            id = cur.fetchone()
            conn.commit()
            if id is Empty:
                pass
            else:
                return id
            self.close_conn(conn)
        except db.DatabaseError as e:
            print Language.MSG_ERR_DATABASE_ERROR.format('73','connecting',e.message)
            pass
        except IOError as e:
            print Language.MSG_ERR_IO_ERROR.format(e.errno, e.strerror)
            pass
        except Exception as e:
            print Language.MSG_ERR_DB_CONNECT.format(e.message)
            pass

    def close_conn(self, con):
        try:
            if con:
                con.close()
        except Exception as e:
            print Language.MSG_ERR_DB_CLOSE.format(e.message())




