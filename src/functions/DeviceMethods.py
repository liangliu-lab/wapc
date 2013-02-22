# coding=utf-8
from Queue import Empty
import json
import os
from time import strftime, gmtime
from src.cli.CommunicationInterface import CommunicationInterface
from src.config.__sql__ import SQL
from src.helper.Utils import Utils
from src.database.db import Database
from src.language.language import Language
from src.model.Commands import Commands
from src.model.Device import Device
from src.model.Request import Request
from src.model.Response import Response
from src.resources.resources import Resources

__author__ = 'fatih'


class DeviceMethods():
    """
        DeviceMethods
    """
    def __init__(self):
        """
        """
        self.utils = Utils()
        self.db = Database()
        self.ci = CommunicationInterface()
        self.script = Resources.ci_script
        self.cfg_device = Resources.cfg_device_resource
        self.now = strftime(Resources.time_format, gmtime())
        self.device = Device()

    def create(self, params):
        """
            Add function to implement a thread at background responds to Web or CLI request
        :param params:
        """
        config = self.device.getConfig()
        resp = Response()
        request = config.getRequest()
        commands = request.getCommands()

        try:
            #check namespace variables if set
            if params.ip:
                self.device.setIP(params.ip.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_IP.format('device')

            if params.name:
                self.device.setName(params.name.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_NAME.format('device')

            if params.description:
                self.device.setDescription(params.description.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_NAME.format('device')

            if params.username:
                self.device.setUsername(params.username.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_USERNAME.format('device')

            if params.password:
                self.device.setPassword(params.password.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_PASSWORD.format('device')

            #gather commands config
            config_source = self.ci.get_source_config(Resources.cfg_device_resource)

            if config_source:
                try:
                    commands = json.loads(unicode(config_source))
                except Exception as e:
                    print e.message
                    pass

            config.setName(self.device.getName())
            config.setIP(self.device.getIP())
            config.setUsername(self.device.getUsername())
            config.setPassword(self.device.getPassword())
            config.setEnablePassword(self.device.getPassword())
            config.setTProtocol(self.device.getConfig().getTProtocol())
            config.setPersonality(self.device.getConfig().getPersonality())

            #set request
            request.setEnable(True)
            request.setConfigure(False)

            #get device recent config
            request.setCommands(commands['show_run']['commands'])

            config.setRequest(request.__dict__)
            self.device.setConfig(config.__dict__)
            print "Request generating..."
            self.ci.write_source_file(config)

            #call communication interface script and gather response - RPC
            try:
                print "Executing device commands please wait..."
                response = unicode(self.ci.call_communication_interface(Resources.ci_source))
                resp = json.loads(
                        unicode(
                            self.ci.call_communication_interface(Resources.ci_source)
                        )
                        .replace('\n',''),
                        encoding='utf-8'
                    )
            except Exception as e:
                print e.message
                pass

            #check if rpc is responded
            if resp:
                #check if wap is connected and returned with success status message 110
                if resp['status'] == 110:
                    cmd = SQL.SQL_INSERT_CONFIG.format(
                        config.getName(),
                        config.getDescription(),
                        config.getIP(),
                        config.getRadiusID(),
                        config.getSSID(),
                        config.getVLAN(),
                        config.getChannel(),
                        config.getChannelFreq(),
                        self.now,
                        self.now
                    )

                    cid = self.db.insert(cmd)
                    if cid:
                        self.device.setConfigID(cid[0])
                        print "New configuration generated for the new device with id: %s" % cid[0]
                    else:
                        print Language.MSG_ERR_EMPTY_CONFIG

                    #insert new device to the database
                    cmd = SQL.SQL_INSERT_DEVICE.format(
                        self.device.getName(),
                        self.device.getDescription(),
                        self.device.getIP(),
                        cid[0],
                        self.device.getUsername(),
                        self.device.getPassword(),
                        self.now,
                        self.now
                    )

                    #get inserted device id and inform user
                    id = self.db.insert(cmd)
                    if id:
                        #write recent config into backup file
                        self.ci.backup(commands, config.getName(), self.now)
                        print Language.MSG_ADD_NEW.format('device', id[0], self.device.getName())

                    #remove input.json
                    #os.remove(Resources.ci_source)
                else:
                    print Language.MSG_ERR_COMM_INTERFACE_CONNECTED_BUT_FAILED.format(resp['message'])
                    pass
            else:
                print Language.MSG_ERR_COMM_INTERFACE_FAILED
                pass
        except Exception as e:
            print e.message
            pass

    def read(self, id):
        """

        :param id:
        """
        cmd = None
        flag = False

        try:
            #check namespace variables if set

            #moderate type value to determine the statement
            cmd = SQL.SQL_SELECT_DEVICE.format(id)
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
        device = Device()
        try:
            if params.id:
                did = params.id.rstrip().lstrip()
                rset = self.read(did)
                data = dict(map(list, zip(rset['fields'], rset['results'])))

                if params.name:
                    device.setName(params.name.rstrip().lstrip())
                else:
                    device.setName(data["name"])

                if params.ip:
                    device.setIP(params.ip.rstrip().lstrip())
                else:
                    device.setIP(data["ip"])

                if params.description:
                    device.setDescription(params.description.rstrip().lstrip())
                else:
                    device.setDescription(data["description"])

                if params.config:
                    device.setConfigID(params.config.rstrip().lstrip())
                else:
                    device.setConfigID(data["config"])

                if params.username:
                    device.setUsername(params.username.rstrip().lstrip())
                else:
                    device.setUsername(data["username"])

                if params.password:
                    device.setPassword(params.password.rstrip().lstrip())
                else:
                    device.setPassword(data["password"])

                cmd = SQL.SQL_UPDATE_DEVICE % \
                      {
                          "name": device.getName(),
                          "ip": device.getIP(),
                          "description": device.getDescription(),
                          "config_id": int(device.getConfigID()),
                          "username": device.getUsername(),
                          "password": device.getPassword(),
                          "modified": self.now,
                          "id": int(did)
                      }

                if self.db.update(cmd):
                    print Language.MSG_UPDATE_RECORD.format('device', did, group.getName())
                else:
                    print Language.MSG_ERR_DATABASE_ERROR.format(self.utils.get_line(), 'updating recorded group', did)
            else:
                print Language.MSG_ERR_EMPTY_ID
        except Exception as e:
            print e.message

    def delete(self, params):
        """

        """
