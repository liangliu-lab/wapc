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
import threading
from time import strftime, gmtime
from src.cli.CommunicationInterface import CommunicationInterface
from src.resources.SQL import SQL
from src.database.Database import Database
from src.helpers.Utils import Utils
from src.language.Language import Language
from src.resources.Resources import Resources
from src.model.Config import Config


class ConfigMethods(threading.Thread):
    """
    ConfigMethods class aims to provide required methods to requester class
    or methods to read, update Config object.
    """

    def __init__(self, new_config, params):
        """
        Constructor of ConfigMethods

        @param new_config Is a new config tuple object to update self.config
        @param params Is used to set new parameters to recent instance
        """
        super(ConfigMethods, self).__init__()
        self.utils = Utils()
        self.database = Database(Resources.cfg_section_master_db)
        self.log_database = Database(Resources.cfg_section_log_db)
        self.communication_interface = CommunicationInterface()
        self.script = Resources.ci_script
        self.cfg_device = Resources.cfg_device_resource
        self.now = strftime(Resources.time_format, gmtime())

        self.config = Config()
        self.set_config(new_config)

        self.params = None
        self.set_params(params)

    def create(self, params):
        """
        This method is used to create a config independently
        @param params
        """

    def read(self, config_id):
        """
        read method aims to read given config id details from database and
        return them into a result set list.

        @param config_id
        @return result set list includes column names and rows
        """
        try:
            #check namespace variables if set

            #moderate type value to determine the statement
            cmd = SQL.SQL_SELECT_CONFIG_DETAIL % {'id': int(config_id)}
            fields, results = self.database.select(cmd)
            if fields and results:
                rset = {"fields": fields,
                        "results": [list(f) for f in results][0]}
                return rset
            else:
                raise self.database.DatabaseError(
                    Language.MSG_ERR_GENERIC.format(
                        self.utils.get_line(),
                        "There is no config record found on table"))
        except self.database.DatabaseError as exception:
            print exception.message

    def set(self, config):
        """
        Set method will update given config by parameter
        @param config is a Config model which provided by parameter
        """

    def update(self, params):
        """
        Update methods certainly moderated by $ edit [OPTIONS] command by CLI.
        This methods only inherit update database
        records by no touching physical device config.

        @param params
        """
        cmd = None
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

                if self.database.update(cmd):
                    print Language.MSG_UPDATE_RECORD.format(
                        'device', did, config.get_name())
                else:
                    print Language.MSG_ERR_DATABASE_ERROR.format(
                        self.utils.get_line(), 'updating recorded group', did)
            else:
                raise Exception(
                    "Error occured while getting required parameters "
                    "device 'id', option, and param")
        except BufferError as exception:
            print exception.message

    def delete(self, params):
        """

        :param params:
        """

    def show(self, params):
        """

        :param params:
        """

    def set_config(self, config):
        """
        ConfigMethods controller class config setter
        @param config is a Config object includes details
        """
        self.config.update(config)

    def get_config(self):
        """
        ConfigMethods controller class config getter
        @return config is a Config object
        """
        return self.config

    def set_params(self, params):
        """
        ConfigMethods controller class config setter
        @param params is a Config object includes details
        """
        self.params = params

    def get_params(self):
        """
        ConfigMethods controller class config getter
        @return params is a Config object
        """
        return self.params