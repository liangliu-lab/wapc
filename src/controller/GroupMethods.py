# coding=utf-8
from Queue import Empty
from time import strftime, gmtime
from src.config.__sql__ import SQL
from src.cli.CommunicationInterface import CommunicationInterface
from src.database.db import Database
from src.helper.Utils import Utils
from src.language.language import Language
from src.model.Group import Group
from src.resources.resources import Resources

__author__ = 'fatih'


class GroupMethods(object):
    """
        GroupMethods
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
            add new group with params
        :rtype : object
        :param params:
        """
        group = Group()
        try:
            #check namespace variables if set
            if params.name:
                group.setName(params.name.strip())
            else:
                group.setName(raw_input(Language.MSG_ERR_EMPTY_NAME.format('group'),":"))

            if params.description:
                group.setDescription(params.description.strip())
            else:
                print Language.MSG_ERR_EMPTY_DESC.format('group')

            if params.config:
                group.setConfig(params.config)
            else:
                print Language.MSG_ERR_EMPTY_CONFIG.format('group')

            cmd = SQL.SQL_INSERT_GROUP.format(
                group.getName(),
                group.getDescription(),
                group.getConfig(),
                self.now,
                self.now
            )
            gID = self.db.insert(cmd)
            if gID:
                print Language.MSG_ADD_NEW.format('group', gID[0], group.getName())
            else:
                print Language.MSG_ERR_DATABASE_ERROR.format(self.utils.get_line(), 'inserting new group', gID[0])
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    def read(self, gID):
        """

        :param gID:
        """
        try:
            #check namespace variables if set

            #moderate type value to determine the statement
            cmd = SQL.SQL_SELECT_GROUP_DETAIL.format(gID)
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
                    Language.MSG_ERR_GENERIC.format(self.utils.get_line(), "There is no group record found on table"))
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    def getGroupConfig(self, gID):
        """

        :param gID:
        """
        try:
            #check namespace variables if set

            #moderate type value to determine the statement
            cmd = SQL.SQL_SELECT_GROUP_CONFIG % {'group_id': int(gID)}
            fields, results = self.db.select(cmd)
            if fields and results:
                try:
                    rset = {"fields": fields, "results": [list(f) for f in results]}
                    return rset
                except Exception as e:
                    print e.message
                    pass
            else:
                raise Exception(
                    Language.MSG_ERR_GENERIC.format(self.utils.get_line(), "There is no group record found on table"))
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

    def update(self, params):
        """
        :param params:
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

                if self.db.update(cmd):
                    print Language.MSG_UPDATE_RECORD.format('group', params.id, group.getName())
                else:
                    print Language.MSG_ERR_DATABASE_ERROR.format(self.utils.get_line(), 'updating recorded group', did)
            else:
                print Language.MSG_ERR_EMPTY_ID
        except Exception as e:
            print e.message

    def delete(self, params):
        """

        :param params:
        """

    def set(self, params):
        """
            This methods handle options and connect throug device by given name
            Sample command: set -t group -o ssid -i [GROUPID]
        :param params:
        """
        # TODO implement group editing one by one device: done
        # TODO get all devices under given group by SQL: done
        # TODO set update every config file belongs to given device: done

        from src.controller.ConfigMethods import ConfigMethods
        from src.model.Config import Config
        from src.controller.DeviceMethods import DeviceMethods
        import threading
        group = Group()
        config = Config()
        configMethods = ConfigMethods(config, params)
        try:

            if params.option:
                option = params.option.strip()
            else:
                print Language.MSG_ERR_EMPTY_OPTION.format('device')

            if params.id:
                group.setID(params.id.strip())
            else:
                print Language.MSG_ERR_EMPTY_ID.format('device')

            if group.getID() and option:

                print "Your command(s) will be executing... Please enter required command params below:\n"
                #params.interface = raw_input("Enter parameter for interface of required device:").strip()
                params.interface = "0"
                params.param = raw_input("Enter parameter for %(type)s this command of device:"
                                         % {'type': params.option}).strip()

                configSet = self.getGroupConfig(group.getID())
                """
                    This line gather an object like below:
                    {   'fields':
                            [   'Config', 'Device', 'Device Name', 'Config Name', 'description', 'ip', 'radius', 'ssid',
                                'vlan', 'channel', 'frequency', 'maxclients', 'username', 'password', 'enable_password',
                                'transport_protocol', 'personality', 'date_added', 'date_modified'
                            ],
                        'results': [
                            [   23, 45, 'New test2 for demo', 'New test2 for demo', 'Default desc for device',
                                '192.168.0.100',13, '0', 0, 4, 'None', None, 'Cisco', 'Cisco', 'Cisco', 'Telnet', 'ios',
                                datetime.datetime(2013, 3, 6, 13, 52, 14), datetime.datetime(2013, 3, 7, 14, 27, 39)
                            ],
                            [   23, 47, 'Test after a couple hours', 'New test2 for demo', 'Default desc for device',
                                '192.168.0.100', 13, '0', 0, 4, 'None', None, 'Cisco', 'Cisco', 'Cisco', 'Telnet', 'ios',
                                datetime.datetime(2013, 3, 6, 13, 52, 14), datetime.datetime(2013, 3, 7, 14, 27, 39)
                            ]
                        ]
                    }
                """
                """
                    Now convert this object into this
                    [
                    {'username': 'Cisco', 'transport_protocol': 'Telnet', 'Device Name': 'With a fresh breath',
                    'description': 'Default desc for device', 'date_added': datetime.datetime(2013, 3, 8, 9, 32, 13),
                    'date_modified': datetime.datetime(2013, 3, 8, 9, 32, 13), 'ip': '192.168.0.100', 'vlan': 0,
                    'enable_password': 'Cisco', 'Config Name': 'With a fresh breath', 'frequency': '0', 'radius': 0,
                    'personality': 'ios', 'Device': 49, 'maxclients': 0, 'password': 'Cisco', 'Config': 27,
                    'channel': 0, 'ssid': 'LBREAP'},
                    {'username': 'Cisco', 'transport_protocol': 'Telnet', 'Device Name': 'With a fresh breath for
                    second device', 'description': 'Default desc for device',
                    'date_added': datetime.datetime(2013, 3, 8, 9, 33, 57),
                    'date_modified': datetime.datetime(2013, 3, 8, 11, 23, 1),
                    'ip': '192.168.0.35', 'vlan': 0, 'enable_password': 'Cisco',
                    'Config Name': 'With a fresh breath for second device', 'frequency': '0', 'radius': 0,
                    'personality': 'ios', 'Device': 50, 'maxclients': 0, 'password': 'Cisco', 'Config': 28,
                    'channel': 4, 'ssid': 'LBREAP'}
                    ]
                """
                # results cover
                results = [dict(zip(configSet['fields'], result)) for result in configSet['results']]

                for row in results:
                    if 'Add Date' in row:
                        row['Add Date'] = row['Add Date'].strftime(Resources.time_format)
                    if 'Last Modified' in row:
                        row['Last Modified'] = row['Last Modified'].strftime(Resources.time_format)
                    else:
                        raise Exception("Related option you provided could not be found in object definition.")

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
                    'group_id': int(group.getID())
                }
        except Exception as e:
            print e.message
            pass

    def show(self, params):
        """
            Show methods for devices in given group id
            @param params
        """