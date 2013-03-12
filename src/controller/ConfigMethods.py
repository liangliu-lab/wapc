# coding=utf-8
"""
    Config methods controller class
"""
from time import strftime, gmtime
from src.cli.CommunicationInterface import CommunicationInterface
from src.config.__sql__ import SQL
from src.database.db import Database
from src.helper.Utils import Utils
from src.language.language import Language
from src.resources.resources import Resources

__author__ = 'fatih'


class ConfigMethods(object):
    """
        ConfigMethods
    """

    def __init__(self):
        self.utils = Utils()
        self.db = Database()
        self.ci = CommunicationInterface()
        self.script = Resources.ci_script
        self.cfg_device = Resources.cfg_device_resource
        self.now = strftime(Resources.time_format, gmtime())

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
                rset = {"fields": fields, "results": [list(f) for f in results][0]}
                return rset
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

    def show(self, params):
        """

        :param params:
        """
