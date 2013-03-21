# coding=utf-8
"""
    Config methods controller class
"""
import threading
from time import strftime, gmtime
from src.cli.CommunicationInterface import CommunicationInterface
from src.config.__sql__ import SQL
from src.controller.DeviceMethods import DeviceMethods
from src.database.db import Database
from src.helper.Utils import Utils
from src.language.language import Language
from src.resources.resources import Resources
from src.model.Config import Config

__author__ = 'fatih'


class ConfigMethods(threading.Thread):
    """
        ConfigMethods
    """

    def __init__(self, new_config, params):
        super(ConfigMethods, self).__init__()
        self.utils = Utils()
        self.db = Database()
        self.ci = CommunicationInterface()
        self.script = Resources.ci_script
        self.cfg_device = Resources.cfg_device_resource
        self.now = strftime(Resources.time_format, gmtime())

        self.config = Config()
        self.setConfig(new_config)

        self.params = None
        self.setParams(params)

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
                    Language.MSG_ERR_GENERIC.format(self.utils.get_line(), "There is no config record found on table"))
        except Exception as e:
            print e.message
            pass

    def set(self, config):
        """
            Set method will update given config by parameter
            @param config is a Config model which provided by parameter
        """

    def update(self, params):
        """
        Update methods certainly moderated by $ edit [OPTIONS] command by CLI. This methods only inherit update database
        records by no touching physical device config.

        @param params:
        """
        config = Config()
        try:
            if params.id:
                did = params.id.strip()
            else:
                print Language.MSG_ADD_ID_HELP
                did = raw_input("Please enter 'id' value:").strip()

            if params.option:
                option = params.option.strip()
            else:
                print Language.MSG_ADD_OPTION_HELP
                option = raw_input("Please enter 'option' value:").strip()

            if params.param:
                param = params.param.strip()
            else:
                print Language.MSG_ADD_PARAM_HELP
                param = raw_input("Please enter 'param' value:").strip()


            if did and option and param:
                if option in config:
                    cmd = SQL.SQL_UPDATE_DEVICE_CONFIG % \
                          {
                              "key": option,
                              "value": param,
                              "modified": self.now,
                              "id": int(did)
                          }

                if self.db.update(cmd):
                    print Language.MSG_UPDATE_RECORD.format('device', did, config.get_name())
                else:
                    print Language.MSG_ERR_DATABASE_ERROR.format(self.utils.get_line(), 'updating recorded group', did)
            else:
                raise Exception("Error occured while getting required parameters device 'id', option, and param")
        except Exception as e:
            print e.message

    def run(self):
        """
        This methods runs a thread to update pyshical devices by given parameters gathered from database
        """
        while True:
            try:
                deviceMethods = DeviceMethods(self.getConfig())
                if deviceMethods.group_set(self.getConfig(), self.getParams()):
                    break
            except BaseException as e:
                print e.message
                break

    def delete(self, params):
        """

        :param params:
        """

    def show(self, params):
        """

        :param params:
        """

    def setConfig(self, config):
        """
            ConfigMethods controller class config setter
            @param config is a Config object includes details
        """
        self.config.update(config)

    def getConfig(self):
        """
            ConfigMethods controller class config getter
            @return config is a Config object
        """
        return self.config

    def setParams(self, params):
        """
            ConfigMethods controller class config setter
            @param params is a Config object includes details
        """
        self.params = params

    def getParams(self):
        """
            ConfigMethods controller class config getter
            @return params is a Config object
        """
        return self.params