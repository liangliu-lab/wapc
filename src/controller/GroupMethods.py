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

@package ctonroller
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

"""

from time import strftime, gmtime
from src.resources.SQL import SQL
from src.cli.CommunicationInterface import CommunicationInterface
from src.database.Database import Database
from src.helper.Utils import Utils
from src.language.Language import Language
from src.model.Group import Group
from src.resources.Resources import Resources


class GroupMethods(object):
    """
        GroupMethods class includes group oriented methods such group set, group
        unset, group show operations.

        Methods covered by GroupMethods and other controller methods in other
        might be similar each other but in deep they have their own custom
        attributes and variables to determine each process is focused to the
        target.
    """

    def __init__(self):
        self.utils = Utils()
        self.database = Database()
        self.communication_interface = CommunicationInterface()
        self.script = Resources.ci_script
        self.cfg_device = Resources.cfg_device_resource
        self.now = strftime(Resources.time_format, gmtime())

    def create(self, params):
        """
        Create a new group with given details in inventory

        @param params
        """
        group = Group()
        try:
            #check namespace variables if set
            if params.name:
                group.set_name(params.name.strip())
            else:
                group.set_name(
                    raw_input(Language.MSG_ERR_EMPTY_NAME.format('group'),":"))

            if params.description:
                group.set_description(params.description.strip())
            else:
                print Language.MSG_ERR_EMPTY_DESC.format('group')

            if params.config:
                group.set_config(params.config)
            else:
                print Language.MSG_ERR_EMPTY_CONFIG.format('group')

            cmd = SQL.SQL_INSERT_GROUP.format(
                group.get_name(),
                group.get_description(),
                group.get_config(),
                self.now,
                self.now
            )
            group_id = self.database.insert(cmd)
            if group_id:
                print Language.MSG_STATUS_ADD_SUCCESS % \
                      {
                          'type': 'config',
                          'id': group_id[0],
                          'name': group.get_name()
                      }
            else:
                print Language.MSG_ERR_DATABASE_ERROR\
                    .format(self.utils.get_line()
                    , 'inserting new group', group_id[0])
        except RuntimeError as exception:
            print Language.MSG_ERR_GENERIC\
                .format(self.utils.get_line(), exception.message)

    def read(self, group_id):
        """
        Read group detail from Groups table by given id.

        @param group_id
        """
        try:
            #check namespace variables if set

            #moderate type value to determine the statement
            cmd = SQL.SQL_SELECT_GROUP_DETAIL.format(group_id)
            fields, results = self.database.select(cmd)
            if fields and results:
                rset = {
                    "fields": fields,
                    "results": [list(f) for f in results][0]
                }
                return rset
            else:
                raise RuntimeError(
                    Language.MSG_ERR_GENERIC
                    .format(self.utils.get_line(),
                            "There is no group record found on table"))
        except RuntimeError as exception:
            print Language.MSG_ERR_GENERIC\
                .format(self.utils.get_line(), exception.message)

    def get_group_config(self, group_id):
        """
        This method gets configuration details from config table belong to
        given group.

        @param group_id
        """
        try:
            #check namespace variables if set

            #moderate type value to determine the statement
            cmd = SQL.SQL_SELECT_GROUP_CONFIG % {'group_id': int(group_id)}
            fields, results = self.database.select(cmd)
            if fields and results:
                rset = {
                    "fields": fields,
                    "results": [list(f) for f in results][0]
                }
                return rset
            else:
                raise RuntimeError(
                    Language.MSG_ERR_GENERIC
                    .format(self.utils.get_line(),
                            "There is no group record found on table"))
        except RuntimeError as exception:
            print Language.MSG_ERR_GENERIC \
                .format(self.utils.get_line(), exception.message)

    def update(self, params):
        """
        Update the group by given id.

        @param params
        """
        group = Group()
        try:
            if params.id:
                did = params.id.rstrip().lstrip()
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

                cmd = SQL.SQL_UPDATE_GROUP % \
                      {
                          "key": option,
                          "value": param,
                          "modified": self.now,
                          "id": int(did)
                      }

                if self.database.update(cmd):
                    print Language.MSG_UPDATE_RECORD\
                        .format('group', params.id, group.get_name())
                else:
                    print Language.MSG_ERR_DATABASE_ERROR\
                        .format(self.utils.get_line(),
                                'updating recorded group', did)
            else:
                print Language.MSG_ERR_EMPTY_ID
                params.id = raw_input(Language.MSG_ERR_EMPTY_ID.format('group'))
                self.update(params)
        except RuntimeError as exception:
            print exception.message

    def set(self, params):
        """
        This methods handle options and connect throug group devices by
        given name or given id.

        Sample command: set -t group -o ssid -i [GROUPID]
        @param params
        """
        from src.controller.ConfigMethods import ConfigMethods

        group = Group()
        try:

            if params.option:
                option = params.option.strip()
            else:
                print Language.MSG_ERR_EMPTY_OPTION.format('device')

            if params.id:
                group.set_id(params.id.strip())
            else:
                print Language.MSG_ERR_EMPTY_ID.format('device')

            if group.get_id() and option:

                print "Your command(s) will be executing... " \
                      "Please enter required command params below:\n"
                params.interface = "0"
                params.param = raw_input(
                    "Enter parameter for %(type)s this command of device:"
                                         % {'type': params.option}).strip()

                config_set = self.get_group_config(group.get_id())
                # results cover
                results = [dict(zip(config_set['fields'], result))
                           for result in config_set['results']]

                results = self.utils.fix_date(results)

                pool = []
                for conf in results:
                    thread_config = ConfigMethods(conf, params)
                    pool.append(thread_config)

                for thread in pool:
                    thread.start()
                    thread.join()

                # Generate update command
                cmd = SQL.SQL_UPDATE_GROUP_CONFIG % {
                    'key' : option,
                    'value' : params.param,
                    'group_id': int(group.get_id())
                }

                if self.database.update(cmd):
                    print Language.MSG_UPDATE_RECORD \
                        .format('group', params.id, group.get_name())
                else:
                    print Language.MSG_ERR_DATABASE_ERROR \
                        .format(self.utils.get_line(),
                                'updating recorded group', group.get_id())

        except RuntimeError as exception:
            print exception.message

    def unset(self, params):
        """
        This methods handle options and connect throug group devices by
        given name or given id.

        Sample command: set -t group -o ssid -i [GROUPID]
        @param params
        """
        from src.controller.ConfigMethods import ConfigMethods

        group = Group()
        try:

            if params.option:
                option = params.option.strip()
            else:
                print Language.MSG_ERR_EMPTY_OPTION.format('device')

            if params.id:
                group.set_id(params.id.strip())
            else:
                print Language.MSG_ERR_EMPTY_ID.format('device')

            if group.get_id() and option:

                print "Your command(s) will be executing... " \
                      "Please enter required command params below:\n"
                params.interface = "0"
                params.param = raw_input(
                    "Enter parameter for %(type)s this command of device:"
                    % {'type': params.option}).strip()

                config_set = self.get_group_config(group.get_id())

                # results cover
                results = [dict(zip(config_set['fields'], result))
                           for result in config_set['results']]

                results = self.utils.fix_date(results)

                pool = []
                for conf in results:
                    thread_config = ConfigMethods(conf, params)
                    pool.append(thread_config)

                for thread in pool:
                    thread.start()
                    thread.join()

                # Generate update command
                cmd = SQL.SQL_UPDATE_GROUP_CONFIG % {
                    'key' : option,
                    'value' : params.param,
                    'group_id': int(group.get_id())
                }

                if self.database.update(cmd):
                    print Language.MSG_UPDATE_RECORD \
                        .format('group', params.id, group.get_name())
                else:
                    print Language.MSG_ERR_DATABASE_ERROR \
                        .format(self.utils.get_line(),
                                'updating recorded group', group.get_id())
        except RuntimeError as exception:
            print exception.message

    def show(self, params):
        """
            Show methods for devices in given group id
            @param params
        """