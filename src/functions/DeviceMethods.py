# coding=utf-8
from Queue import Empty
import json
import os
import threading
from time import strftime, gmtime
from src.cli.CommunicationInterface import CommunicationInterface
from src.config.__sql__ import SQL
from src.helper.Utils import Utils
from src.database.db import Database
from src.language.language import Language
from src.model.Commands import Commands
from src.model.Device import Device
from src.model.Config import Config
from src.model.Request import Request
from src.model.Response import Response
from src.resources.resources import Resources

__author__ = 'fatih'


class DeviceMethods(threading.Thread):
    """
        DeviceMethods
        +Marka bağımsız temel WAP yönetim uygulaması
        - SSID Ayarları
        - IP ve Network Ayarları
        - Kimlik Doğrulama Ayarları

        - WAP Discovery
        - Kanal Yönetimi
        - Roaming
        - Load Balancing

    + WAP ların 802,1x yetkilendirmesi
    """
    def __init__(self, params):
        """
        """
        self.utils = Utils()
        self.db = Database()
        self.ci = CommunicationInterface()
        self.script = Resources.ci_script
        self.cfg_device = Resources.cfg_device_resource
        self.now = strftime(Resources.time_format, gmtime())
        self.device = Device()
        self.params = params

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
            #===================================
            # check namespace variables if set then set them into device model variables
            #===================================

            # set device ip to connect to the device
            if params.ip:
                self.device.setIP(params.ip.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_IP.format('device')

            # set device name to connect to the device
            if params.name:
                self.device.setName(params.name.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_NAME.format('device')

            # set device description to connect to the device
            if params.description:
                self.device.setDescription(params.description.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_DESC.format('device')

            # set device username to connect to the device
            if params.username:
                self.device.setUsername(params.username.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_USERNAME.format('device')

            # set device password to connect to the device
            if params.password:
                self.device.setPassword(params.password.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_PASSWORD.format('device')

            #gather commands config
            config_source = self.ci.get_source_config(Resources.ci_config)

            # get default config object into a dict
            if config_source:
                try:
                    commands = json.loads(unicode(config_source))
                except Exception as e:
                    print e.message
                    pass

            #set config parameters to relate with device
            config.setName(self.device.getName())
            config.setIP(self.device.getIP())
            config.setUsername(self.device.getUsername())
            config.setPassword(self.device.getPassword())
            config.setEnablePassword(self.device.getPassword())
            config.setTProtocol(self.device.getConfig().getTProtocol())
            config.setPersonality(self.device.getConfig().getPersonality())

            #set request
            request.setEnable(True)
            request.setConfigure(True)

            #get device recent config
            # TODO get default commands change ip and re-write config to file
            request.setCommands(commands['request']['commands'])

            # set request for config object to be called by CI script
            config.setRequest(request.__dict__)

            #set device config to relate each other
            self.device.setConfig(config.__dict__)

            # implement request
            print "Request generating..."
            self.ci.write_source_file(config)

            #call communication interface script and gather response - RPC
            print "Executing device commands please wait..."
            resp = json.loads(
                    unicode(
                        self.ci.call_communication_interface(Resources.ci_source)
                    )
                    .replace('\n',''),
                    encoding='utf-8'
                )
            #check if rpc is responded
            if resp:
                #check if wap is connected and returned with success status message 110
                if resp['status'] == 110:
                    cmd = SQL.SQL_INSERT_CONFIG % {
                        "name" : config.getName(),\
                        "description" : config.getDescription(), \
                        "ip" : config.getIP(), \
                        "radius_config_id" : config.getRadiusID(), \
                        "ssid" : config.getSSID(), \
                        "vlan_id" : config.getVLAN(), \
                        "channel" : config.getChannel(), \
                        "channel_freq" : config.getChannelFreq(), \
                        "username" : config.getUsername(), \
                        "password" : config.getPassword(), \
                        "enable_password" : config.getEnablePassword(), \
                        "transport_protocol" : config.getTProtocol(), \
                        "personality" : config.getPersonality(), \
                        "date_added" : self.now, \
                        "date_modified" : self.now
                    }

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
        try:
            #check namespace variables if set

            #moderate type value to determine the statement
            cmd = SQL.SQL_SELECT_DEVICE % {'id': int(id)}
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
                    print Language.MSG_UPDATE_RECORD.format('device', did, device.getName())
                else:
                    print Language.MSG_ERR_DATABASE_ERROR.format(self.utils.get_line(), 'updating recorded group', did)
            else:
                print Language.MSG_ERR_EMPTY_ID
        except Exception as e:
            print e.message

    def delete(self, params):
        """

        """

    def set(self, params):
        """
            This methods handle options and connect throug device by given name
        :param params:
        """
        from src.functions.ConfigMethods import ConfigMethods
        config = self.device.getConfig()
        resp = Response()
        request = config.getRequest()
        commands = request.getCommands()
        device = Device()
        config = Config()
        configMethods = ConfigMethods()
        try:
            if params.option:
                option = params.option.rstrip().lstrip()
            else:
                print Language.MSG_ERR_EMPTY_OPTION.format('device')

            if params.id:
                device.setID(params.id.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_ID.format('device')

            if device.getID():
                #gather device detail
                rsetDevice = self.read(device.getID())
                dataDevice = dict(map(list, zip(rsetDevice['fields'], rsetDevice['results'])))
                dataDevice["added"] = dataDevice["added"].strftime(Resources.time_format)
                dataDevice["modified"] = dataDevice["modified"].strftime(Resources.time_format)
                device.update(dataDevice)

                rsetConfig = configMethods.read(dataDevice["config"])
                dataConfig = dict(map(list, zip(rsetConfig['fields'], rsetConfig['results'])))
                dataConfig["date_added"] = dataConfig["date_added"].strftime(Resources.time_format)
                dataConfig["date_modified"] = dataConfig["date_modified"].strftime(Resources.time_format)
                config.update(dataConfig)

                #set device config by updated config
                device.setConfig(config)

                #gather commands config file content
                config_source = self.ci.get_source_config(Resources.cfg_device_resource)

                #check config source and load inside data
                if config_source:
                    try:
                        #turn into dictionary from json
                        commands = json.loads(unicode(config_source))
                    except Exception as e:
                        print e.message
                        pass

                # set config variables
                config.setName(device.getName())
                config.setIP(device.getIP())
                config.setUsername(device.getUsername())
                config.setPassword(device.getPassword())
                config.setEnablePassword(dataConfig["enable_password"])
                config.setTProtocol(dataConfig["transport_protocol"])
                config.setPersonality(dataConfig["personality"])

                #set request
                print "Request generating..."

                #gather interface and params
                print "Your command(s) will be executing... Please enter required command params below:\n"
                interface = raw_input("Enter parameter for interface of required device:")
                new_param = raw_input("Enter parameter for %(type)s this command of device:" % {'type': params.option})

                # TODO get interfaces and unset its ssid
                if 'pre' in commands[str('set_'+option)]:
                    pre = commands[str('set_'+option)]['pre']
                    print "Prerequesting command(s) being executed. Please wait...\n"
                    request.setCommands(commands[str(pre + '_'+ option)]['commands'])
                    request.setEnable(commands[str(pre + '_'+ option)]['enable'])
                    request.setConfigure(commands[str(pre + '_'+ option)]['configure'])

                    for p in request['commands']:
                        if 'param' in p:
                            #new param has been approved??
                            if p["type"]:
                                if p["type"] == "interface":
                                    p["command"] = p["command"] + interface.rstrip().lstrip()
                                elif p["type"] == params.option.rstrip().lstrip():
                                    p["command"] = p["command"] + new_param.rstrip().lstrip()
                                else:
                                    p["command"] = p["command"] + new_param.rstrip().lstrip()
                            #print p["command"]

                    #set config request to generate input.json file
                    config.setRequest(request)

                    #write config model into input.json file
                    self.ci.write_source_file(config)

                    #call communication interface script and gather response - RPC
                    print "Executing device commands please wait..."
                    resp = json.loads(
                        unicode(
                            self.ci.call_communication_interface(Resources.ci_source)
                        )
                        .replace('\n',''),
                        encoding='utf-8'
                    )

                    #check if rpc is responded and shows that prereques command successfully executed
                    if resp:
                        #check if wap is connected and returned with success status message 110
                        if resp['status'] == 110:
                            print "Pre-request command(s) successfully executed"


                request.setCommands(commands[str('set_'+option)]['commands'])
                request.setEnable(commands[str('set_'+option)]['enable'])
                request.setConfigure(commands[str('set_'+option)]['configure'])

                for p in request['commands']:
                    if 'param' in p:
                        if p["type"]:
                            if p["type"] == "interface":
                                p["command"] = p["command"] + interface.rstrip().lstrip()
                            elif p["type"] == params.option.rstrip().lstrip():
                                p["command"] = p["command"] + new_param.rstrip().lstrip()
                            else:
                                p["command"] = p["command"] + new_param.rstrip().lstrip()
                        #print p["command"]

                    #set config request to generate input.json file
                config.setRequest(request)

                #write config model into input.json file
                self.ci.write_source_file(config)

                #call communication interface script and gather response - RPC
                print "Executing device commands please wait..."
                resp = json.loads(
                    unicode(
                        self.ci.call_communication_interface(Resources.ci_source)
                    )
                    .replace('\n',''),
                    encoding='utf-8'
                )

                #check if rpc is responded
                if resp:
                    #check if wap is connected and returned with success status message 110
                    if resp['status'] == 110:
                        cmd = SQL.SQL_UPDATE_CONFIG % {
                            'key': option,
                            'value': new_param,
                            'modified': self.now,
                            'id': config.getID()
                        }

                        #insert updated config and gather inserted record id
                        self.db.update(cmd)
                        os.remove(Resources.ci_source)
                    else:
                        print Language.MSG_ERR_COMM_INTERFACE_CONNECTED_BUT_FAILED.format(resp['message'])
                        pass
                else:
                    print Language.MSG_ERR_COMM_INTERFACE_FAILED
                    pass
            else:
                pass
        except Exception as e:
            print e.message
            pass

    def run(self):
        """
            This methods runs a thread to update pyshical devices by given parameters gathered from database
            :param params:
        """
        while (true):
            self.set(self.params)

    # this method works fine do not touch it!!!
    def show(self, params):
        from src.functions.ConfigMethods import ConfigMethods
        config = self.device.getConfig()
        resp = Response()
        request = config.getRequest()
        commands = request.getCommands()
        device = Device()
        config = Config()
        configMethods = ConfigMethods()
        try:
            if params.option:
                option = params.option.rstrip().lstrip()
            else:
                print Language.MSG_ERR_EMPTY_OPTION.format('device')

            if params.id:
                device.setID(params.id.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_ID.format('device')

            if device.getID():
                #gather device detail
                rsetDevice = self.read(device.getID())
                dataDevice = dict(map(list, zip(rsetDevice['fields'], rsetDevice['results'])))
                dataDevice["added"] = dataDevice["added"].strftime(Resources.time_format)
                dataDevice["modified"] = dataDevice["modified"].strftime(Resources.time_format)
                device.update(dataDevice)

                rsetConfig = configMethods.read(dataDevice["config"])
                dataConfig = dict(map(list, zip(rsetConfig['fields'], rsetConfig['results'])))
                dataConfig["date_added"] = dataConfig["date_added"].strftime(Resources.time_format)
                dataConfig["date_modified"] = dataConfig["date_modified"].strftime(Resources.time_format)
                config.update(dataConfig)

                #set device config by updated config
                device.setConfig(config)

                #gather commands config file content
                config_source = self.ci.get_source_config(Resources.cfg_device_resource)

                #check config source and load inside data
                if config_source:
                    try:
                        #turn into dictionary from json
                        commands = json.loads(unicode(config_source))
                    except Exception as e:
                        print e.message
                        pass

                # set config variables
                config.setName(device.getName())
                config.setIP(device.getIP())
                config.setUsername(device.getUsername())
                config.setPassword(device.getPassword())
                config.setEnablePassword(dataConfig["enable_password"])
                config.setTProtocol(dataConfig["transport_protocol"])
                config.setPersonality(dataConfig["personality"])

                #set request
                print "Request generating..."

                request.setCommands(commands[str('show_'+option)]['commands'])
                request.setEnable(commands[str('show_'+option)]['enable'])
                request.setConfigure(commands[str('show_'+option)]['configure'])

                #set config request to generate input.json file
                config.setRequest(request)

                #write config model into input.json file
                self.ci.write_source_file(config)

                #call communication interface script and gather response - RPC
                print "Executing device commands please wait..."
                resp = json.loads(
                    unicode(
                        self.ci.call_communication_interface(Resources.ci_source)
                    )
                    .replace('\n',''),
                    encoding='utf-8'
                )

                #check if rpc is responded
                if resp:
                    #check if wap is connected and returned with success status message 110
                    if resp['status'] == 110:
                        print resp['message']
                        os.remove(Resources.ci_source)
                    else:
                        print Language.MSG_ERR_COMM_INTERFACE_CONNECTED_BUT_FAILED.format(resp['message'])
                        pass
                else:
                    print Language.MSG_ERR_COMM_INTERFACE_FAILED
                    pass
            else:
                pass
        except Exception as e:
            print e.message
            pass


