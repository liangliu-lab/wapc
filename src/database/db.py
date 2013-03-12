# coding=utf-8
"""
This file will be used to implement database interactions with postgresql

"""
from Queue import Empty
import ConfigParser
import psycopg2 as db
from src.helper.Utils import Utils
from src.language.language import Language
from src.resources.resources import Resources


__author__ = 'fatih'


class Database(object):
    """
        Database class implement a database interface between application and postgresql
    """

    def __init__(self):
        """

        """
        self.__config__ = Resources.__db__config__
        self.__section__ = Resources.cfg_section_postgre
        self.utils = Utils()

    def connect(self):
        """
            Connect database with given parameters
        :rtype : object
        """
        try:
            config = ConfigParser.RawConfigParser()
            config.read(self.__config__)
            #gather connection parameters from database config file
            db_name = config.get(self.__section__, 'db_name')
            user = config.get(self.__section__, 'username')
            password = config.get(self.__section__, 'password')
            host = config.get(self.__section__, 'host')
            connStr = "dbname=" + db_name + " user=" + user + " password=" + password + " host=" + host
            conn = db.connect(connStr)
            return conn
        except db.DatabaseError as e:
            print Language.MSG_ERR_DATABASE_ERROR.format(self.utils.get_line(), 'connecting', e.message)
            pass
        except ConfigParser.NoSectionError as e:
            print Language.MSG_ERR_NO_CONFIG_SECTION.format(e.message)
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
        :param cmd:
        """
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(cmd)
            fields = [i[0] for i in cur.description]
            results = cur.fetchall()
            conn.commit()
            print Language.MSG_SUCCESS_SELECT
            return fields, results
        except db.DatabaseError as e:
            print Language.MSG_ERR_DATABASE_ERROR.format(self.utils.get_line(), 'selecting', e.message)
            pass
        except IOError as e:
            print Language.MSG_ERR_IO_ERROR.format(e.errno, e.strerror)
            pass
        except Exception as e:
            print Language.MSG_ERR_DB_CONNECT.format(e.message)
            pass
        finally:
            self.close_conn(conn)

    def insert(self, cmd):
        """
            Insert objects to database
            expected json formats for inserting objects
        :param cmd:
        """
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(cmd)
            rid = cur.fetchone()
            conn.commit()
            if rid is Empty:
                pass
            else:
                return rid
        except db.DatabaseError as e:
            print Language.MSG_ERR_DATABASE_ERROR.format(self.utils.get_line(), 'inserting', e.message)
            pass
        except IOError as e:
            print Language.MSG_ERR_IO_ERROR.format(e.errno, e.strerror)
            pass
        except Exception as e:
            print Language.MSG_ERR_DB_CONNECT.format(e.message)
            pass
        finally:
            self.close_conn(conn)

    def update(self, cmd):
        """
            Update database objects with given values
        :param cmd:
        """
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(cmd)
            conn.commit()
            return True
        except db.DatabaseError as e:
            print Language.MSG_ERR_DATABASE_ERROR.format(self.utils.get_line(), 'updating', e.message)
            return False
            pass
        except IOError as e:
            print Language.MSG_ERR_IO_ERROR.format(e.errno, e.strerror)
            return False
            pass
        except Exception as e:
            print Language.MSG_ERR_DB_CONNECT.format(e.message)
            return False
            pass
        finally:
            self.close_conn(conn)

    def remove(self, cmd):
        """
            Remove objects from given tables
        :param cmd:
        """
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(cmd)
            conn.commit()
            print Language.MSG_SUCCESS_REMOVE
        except db.DatabaseError as e:
            print Language.MSG_ERR_DATABASE_ERROR.format(self.utils.get_line(), 'updating', e.message)
            pass
        except IOError as e:
            print Language.MSG_ERR_IO_ERROR.format(e.errno, e.strerror)
            pass
        except Exception as e:
            print Language.MSG_ERR_DB_CONNECT.format(e.message)
            pass
        finally:
            self.close_conn(conn)

    def close_conn(self, con):
        """

        :param con:
        """
        try:
            if con:
                con.close()
        except Exception as e:
            print Language.MSG_ERR_DB_CLOSE.format(e.message)




