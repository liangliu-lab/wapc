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
import socket
import threading
import Queue

from time import strftime, gmtime
from src.controller.DeviceMethods import DeviceMethods
from src.resources.SQL import SQL
from src.cli.CommunicationInterface import CommunicationInterface
from src.database.Database import Database
from src.helpers.Utils import Utils
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
        self.database = Database(Resources.cfg_section_master_db)
        self.log_database = Database(Resources.cfg_section_log_db)
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
                print Language.MSG_ERR_EMPTY_NAME.format('group')
                group.set_name(
                    raw_input("Please enter an nick name for group:").strip())

            if params.description:
                group.set_description(params.description.strip())
            else:
                print Language.MSG_ERR_EMPTY_DESC.format('group')

            if params.config:
                group.set_config_id(params.config)
            else:
                print Language.MSG_ERR_EMPTY_CONFIG.format('group')

            cmd = SQL.SQL_INSERT_GROUP.format(
                group.get_name(),
                group.get_description(),
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
        except BaseException as exception:
            raise BaseException("An error occurred: %s" % {exception.message})

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
        except BaseException as exception:
            raise BaseException("An error occurred: %s" % {exception.message})

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
                    "results": [list(f) for f in results]
                }
                return rset
            else:
                raise RuntimeError(
                    Language.MSG_ERR_GENERIC
                    .format(self.utils.get_line(),
                            "There is no group record found on table"))
        except BaseException as exception:
            raise BaseException("An error occurred: %s" % {exception.message})

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

                self.database.update(cmd)
            else:
                print Language.MSG_ERR_EMPTY_ID
                params.id = raw_input(Language.MSG_ERR_EMPTY_ID.format('group'))
                self.update(params)
        except BaseException as exception:
            raise BaseException("An error occurred: %s" % {exception.message})

    def set(self, params):
        """
        This methods handle options and connect throug group devices by
        given name or given id.

        Sample command: set -t group -o ssid -i [GROUPID]
        @param params
        """

        try:
            params.command = "set"
            self.exec_group(params)
        except BaseException as exception:
            raise BaseException("An error occurred: %s" % {exception.message})

    def unset(self, params):
        """
        This methods handle options and connect throug group devices by
        given name or given id.

        Sample command: set -t group -o ssid -i [GROUPID]
        @param params
        """
        try:
            params.command = "unset"
            self.exec_group(params)
        except BaseException as exception:
            raise BaseException("An error occurred: %s" % {exception.message})

    def show(self, params):
        """
            Show methods for devices in given group id
            @param params
        """
        try:
            params.command = "show"
            self.exec_group(params)
        except BaseException as exception:
            raise BaseException("An error occurred: %s" % {exception.message})

    def exec_group(self, params):
        """
        Execute group commands
        @param params gathered params by command line arguments
        @return
        """
        group = Group()
        try:
            if params.option:
                option = params.option.strip()
            else:
                print Language.MSG_ERR_EMPTY_OPTION.format('group')
                option = raw_input("Please enter an option to be set:")

            if params.id:
                group.set_id(params.id.strip())
            else:
                print Language.MSG_ERR_EMPTY_ID.format('device')
                group.set_id(
                    raw_input("Please enter id for device will be set:"))

            return_response = None
            if group.get_id() and option:
                print "Your command(s) will be executing... " \
                      "Please enter required command params below\n"
                params.interface = "0"
                if params.command != "show":
                    params.param = raw_input(
                        "Enter parameter for %(type)s this command of device:"
                        % {'type': params.option}).strip()

                config_set = self.get_group_config(group.get_id())
                # results cover
                results = [dict(zip(config_set['fields'], result))
                           for result in config_set['results']]

                results = self.utils.fix_date(results)

                device_methods = DeviceMethods(params)
                pool = []
                thread_results = []
                heading = ["id", "name", "ip", "request", "status", "response"]

                queue = Queue.Queue()
                for conf in results:
                    #device_methods.group(params, queue, conf)
                    thread_config = threading.Thread(
                        target=device_methods.group,
                        name=conf["Device"],
                        args=[params, queue, conf],
                    )
                    pool.append(thread_config)

                for thread in pool:
                    thread.start()
                    response = queue.get()
                    thread_results.append(response)

                for thread in pool:
                    thread.join()

                return_response = self.utils.formatter(heading, thread_results)
                # Generate update command
                if params.command is not "show":
                    cmd = SQL.SQL_UPDATE_GROUP_CONFIG % {
                        'key': option,
                        'value': params.param,
                        'group_id': int(group.get_id())
                    }
                    self.database.update(cmd)
            return return_response
        except BaseException as exception:
            raise ("An error occurred: %s" % {exception.message})