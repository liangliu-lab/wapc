# coding=utf-8
from src.config.__sql__ import SQL
from src.database.db import Database
from src.helper.Utils import Utils
from src.language.language import Language

__author__ = 'fatih'


class ConfigMethods(object):
    """
        ConfigMethods
    """

    def __init__(self):
        self.utils = Utils()
        self.db = Database()

    def create(self, params):
        """

        :param params:
        """

    def read(self, config_id):
        """

        :param config_id:
        """
        try:
            #check namespace variables if set

            #moderate type value to determine the statement
            cmd = SQL.SQL_SELECT_CONFIG_DETAIL % {'id': int(config_id)}
            fields, results = self.db.select(cmd)
            if fields and results:
                try:
                    rset = {"fields": fields, "results": [list(f) for f in results][0]}
                    return rset
                except Exception as e:
                    print e.message
                    pass
            else:
                raise Exception(
                    Language.MSG_ERR_GENERIC.format(self.utils.get_line(), "There is no device record found on table"))
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    def update(self, params):
        """

        :param params:
        """

    def delete(self, params):
        """

        :param params:
        """
