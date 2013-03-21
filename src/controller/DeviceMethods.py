# coding=utf-8
"""
    Device methods controller class
"""
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
from string import Template

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
        self.params = params

    def create(self, params):
        """
            Add function to implement a thread at background responds to Web or CLI request
        :param params:
        """
        device = Device()
        config = device.get_config()
        request = config.get_request()
        commands = request.getCommands()

        try:
            #===================================
            # check namespace variables if set then set them into device model variables
            #===================================

            # set device ip to connect to the device
            if params.ip:
                device.set_ip(params.ip.strip())
            else:
                print Language.MSG_ERR_EMPTY_IP.format('device')
                device.set_ip(raw_input("Please enter an IP address:"))

            # set device name to connect to the device
            if params.name:
                device.set_name(params.name.strip())
            else:
                print Language.MSG_ERR_EMPTY_NAME.format('device')
                device.set_name(raw_input("Please enter an nick name:"))

            # set device description to connect to the device
            if params.description:
                device.set_description(params.description.strip())
            else:
                print Language.MSG_ERR_EMPTY_DESC.format('device')

            # set device username to connect to the device
            if params.username:
                device.set_username(params.username.strip())
            else:
                print Language.MSG_ERR_EMPTY_USERNAME.format('device')
                device.set_username(raw_input("Please enter an username:"))

            # set device password to connect to the device
            if params.password:
                device.set_password(params.password.strip())
            else:
                print Language.MSG_ERR_EMPTY_PASSWORD.format('device')
                device.set_password(raw_input("Please enter a password:"))

            # define config file path to initial a new device
            # ==============================================
            # concluded path should be like this at the end:
            # config/[brand]/[model]/[firmware]/[relatoion]-config.conf
            # if no params provided at least brand required and the final pathshould be below:
            # config/[brand]/default/default/slave-config.conf
            # ==============================================
            path = None
            if params.brand:
                device.set_brand(str(params.brand.strip()).lower())
                if params.model:
                    device.set_model(str(params.model.strip()).lower())
                    if params.firmware:
                        device.set_firmware(str(params.firmware.strip()).lower())
                        path = device.get_brand() + "/" + \
                               device.get_model() + "/" + \
                               device.get_firmware()
                    else:
                        path = device.get_brand() + "/" + \
                               device.get_model() + "/default"
                else:
                    # path = params.model.rstript().lstrip()
                    path = device.get_brand() + "/default/default"
            else:
                print (
                    "It must be provided at least brand to identify " \
                    "which device you would like to add to the inventory. See help below:\n" \
                    + Language.MSG_ADD_BRAND_HELP + \
                    "\nPlease use 'help' command to see detailed usage." \
                )
                device.set_brand(raw_input("Please enter a brand:").lower())
                if params.model:
                    device.set_model(str(params.model.strip()).lower())
                    if params.firmware:
                        device.set_firmware(str(params.firmware.strip()).lower())
                        path = device.get_brand() + "/" + \
                               device.get_model() + "/" + \
                               device.get_firmware()
                    else:
                        path = device.get_brand() + "/" + \
                               device.get_model() + "/default"
                else:
                    # path = params.model.rstript().lstrip()
                    path = device.get_brand() + "/default/default"

            if params.relation:
                device.set_relation(str(params.relation.strip()).lower())
            else:
                print "You did not provide a relation such as one of 'master' or 'slave'. " \
                      "Therefore, the default value is set to 'slave'."


            #gather commands config
            # config_source = self.ci.get_source_config(Resources.ci_config)
            if path and device.get_relation():
                # set default config file path
                config_source_file = Resources.device_initial_config % \
                                     {'path': path, 'relation': device.get_relation()}

                # get default config file content
                config_source = self.ci.get_source_config(config_source_file)

                # replace ipaddress in file content
                config_source = config_source.replace('###', device.get_ip())

                # write new content into default config file
                tftp_target = Resources.device_tftp_path % { 'relation': device.get_relation()}
                self.ci.write_source_file(config_source, tftp_target, 'RAW')
            else:
                raise Exception(
                    "Device config path could not be found or not correctly configured please check given parameters" \
                    "then try again. Here is recent path: " + Resources.device_initial_config %
                                                            {'path': path, 'relation': device.get_relation()})

            # get default config object into a dict
            if config_source:
                # replace recent ip in config file and generate commands
                commands = json.loads(unicode(self.ci.get_source_config(Resources.device_load_command)))
                commands['commands'][0]['command'] = commands['commands'][0]['command'] % \
                                                     { 'file': Resources.device_tftp_file %
                                                               {'relation': device.get_relation() }
                                                     }
                #commands = json.loads(unicode(config_source))
            else:
                raise Exception(
                    "Error occured while getting config source to read and send commands to the device." \
                    "Please try again.")

            #set config parameters to relate with device
            config.set_name(device.get_name())
            config.set_username(device.get_username())
            config.set_password(device.get_password())
            config.set_ip(device.get_ip())
            config.set_enable_password(config.get_password())
            config.set_transport_protocol(device.get_config().get_transport_protocol())
            config.set_personality(device.get_config().get_personality())

            #set request
            request.setEnable(True)
            request.setConfigure(False)

            #get device recent config
            request.setCommands(commands['commands'])

            # set request for config object to be called by CI script
            config.set_request(request.__dict__)

            #set device config to relate each other
            device.set_config(config.__dict__)

            # destroy variables no need them longer
            del request
            del config_source_file
            del tftp_target
            del path
            del commands

            # implement request
            print "Request generating..."
            # ======================================
            # Write config object into file with write_source_file method with parameter source and source type
            # Source type can be JSON or RAW or XML
            # ======================================
            self.ci.write_source_file(config, Resources.ci_source, 'JSON')

            #call communication interface script and gather response - RPC
            print "Executing device commands please wait..."
            resp = json.loads(
                    unicode(
                        self.ci.call_communication_interface(Resources.ci_source)
                    )
                    .replace('\n',''),
                    encoding='utf-8'
                )
            #remove input.json
            os.remove(Resources.ci_source)

            #check if rpc is responded
            if resp:
                #check if wap is connected and returned with success status message 110
                if resp['status'] == 110:
                    cmd = SQL.SQL_INSERT_CONFIG % {
                        "name" : config.get_name(),\
                        "description" : config.get_description(), \
                        "ip" : config.get_ip(), \
                        "radius_config_id" : config.get_radius(), \
                        "ssid" : config.get_ssid(), \
                        "vlan_id" : config.get_vlan(), \
                        "channel" : config.get_channel(), \
                        "channel_freq" : config.getChannelFreq(), \
                        "maxclients": config.get_maxclient(), \
                        "username" : config.get_username(), \
                        "password" : config.get_password(), \
                        "enable_password" : config.get_enable_password(), \
                        "transport_protocol" : config.get_transport_protocol(), \
                        "personality" : config.get_personality(), \
                        "date_added" : self.now, \
                        "date_modified" : self.now
                    }

                    # insert new config record to database then get its row id
                    cid = self.db.insert(cmd)

                    if cid:
                        device.set_config_id(cid[0])
                        print "New configuration generated for the new device with id: %s" % cid[0]
                        #insert new device to the database
                        cmd = SQL.SQL_INSERT_DEVICE % {
                            "name" : device.get_name(),
                            "username": device.get_username(),
                            "password": device.get_password(),
                            "desc": device.get_description(),
                            "ip" : device.get_ip(),
                            "config" : int(cid[0]),
                            "brand" : device.get_brand(),
                            "model" : device.get_model(),
                            "firmware" : device.get_firmware(),
                            "relation" : device.get_relation(),
                            "date_added" : self.now,
                            "date_modified" : self.now
                        }

                        #get inserted device id and inform user
                        new_id = self.db.insert(cmd)
                        if new_id:
                            #write recent config into backup file
                            self.ci.backup(config_source, config.get_name(), self.now, 'RAW')
                            print Language.MSG_ADD_NEW.format('device', new_id[0], device.get_name())
                    else:
                        raise Exception(
                            Language.MSG_ERR_DATABASE_INSERT
                        )
                else:
                    print Language.MSG_ERR_COMM_INTERFACE_CONNECTED_BUT_FAILED.format(resp['message'])
                    pass
            else:
                print Language.MSG_ERR_COMM_INTERFACE_FAILED
                pass
        except Exception as e:
            print e.message
            pass

    def read(self, cid):
        """

        :param id:
        """
        try:
            #check namespace variables if set

            #moderate type value to determine the statement
            cmd = SQL.SQL_SELECT_DEVICE % {'id': int(cid)}
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
        Update methods certainly moderated by $ edit [OPTIONS] command by CLI. This methods only inherit update database
        records by no touching physical device config.
        @params Params comes from main class
        """
        device = Device()
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
                if option in device:
                    cmd = SQL.SQL_UPDATE_DEVICE % \
                          {
                              "key": option,
                              "value": param,
                              "modified": self.now,
                              "id": int(did)
                          }
                else:
                    cmd = SQL.SQL_UPDATE_DEVICE_CONFIG % \
                          {
                              "key": option,
                              "value": param,
                              "modified": self.now,
                              "id": int(did)
                          }

                if self.db.update(cmd):
                    print Language.MSG_UPDATE_RECORD.format('device', did, device.get_name())
                else:
                    print Language.MSG_ERR_DATABASE_ERROR.format(self.utils.get_line(), 'updating recorded group', did)
            else:
                raise Exception("Error occured while getting required parameters device 'id', option, and param")
        except Exception as e:
            print e.message

    def delete(self, params):
        """

        """

    # this method works fine do not touch it!!!
    def set(self, params):
        """
            This methods handle options and connect throug device by given name
        :param params:
        """
        from src.controller.ConfigMethods import ConfigMethods
        device = Device()
        config = Config()
        request = config.get_request()
        commands = request.getCommands()
        configMethods = ConfigMethods(config, params)
        try:
            if params.option:
                option = params.option.strip()
            else:
                print Language.MSG_ERR_EMPTY_OPTION.format('device')
                option = raw_input("Please enter an option to be set:")

            if params.id:
                device.set_id(params.id.strip())
            else:
                print Language.MSG_ERR_EMPTY_ID.format('device')
                device.set_id(raw_input("Please enter id for device will be set:"))

            if device.get_id():
                #gather device detail
                rsetDevice = self.read(device.get_id())
                dataDevice = dict(map(list, zip(rsetDevice['fields'], rsetDevice['results'])))
                dataDevice["Add Date"] = dataDevice["Add Date"].strftime(Resources.time_format)
                dataDevice["Last Modified"] = dataDevice["Last Modified"].strftime(Resources.time_format)
                device.update(dataDevice)

                rsetConfig = configMethods.read(dataDevice["Configuration"])
                dataConfig = dict(map(list, zip(rsetConfig['fields'], rsetConfig['results'])))
                dataConfig["Add Date"] = dataConfig["Add Date"].strftime(Resources.time_format)
                dataConfig["Last Modified"] = dataConfig["Last Modified"].strftime(Resources.time_format)
                config.update(dataConfig)

                #set device config by updated config
                device.set_config(config)

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

                #set request
                print "Request generating..."

                #gather interface and params
                print "Your command(s) will be executing... Please enter required command params below:\n"
                interface = raw_input("Enter parameter for interface of required device:")
                new_param = raw_input("Enter parameter for %(type)s this command of device:" % {'type': params.option})

                # set new value to given variable where option is its attribute
                #config[option] = new_param

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
                                    p["command"] = p["command"] + interface.strip()
                                elif p["type"] == params.option.strip():
                                    p["command"] = p["command"] + config.get_ssid()
                                else:
                                    p["command"] = p["command"] + config.get_ssid()
                            #print p["command"]

                    #set config request to generate input.json file
                    config.set_request(request)

                    #write config model into input.json file
                    self.ci.write_source_file(config, Resources.ci_source, 'JSON')

                    #call communication interface script and gather response - RPC
                    print "Executing device commands please wait..."
                    resp = json.loads(
                        unicode(
                            self.ci.call_communication_interface(Resources.ci_source)
                        )
                        .replace('\n',''),
                        encoding='utf-8'
                    )

                    #remove input.json
                    os.remove(Resources.ci_source)

                    #check if rpc is responded and shows that prereques command successfully executed
                    if resp:
                        #check if wap is connected and returned with success status message 110
                        if resp['status'] == 110:
                            print "Pre-request command(s) successfully executed"

                config[option] = new_param.strip()

                request.setCommands(commands[str('set_'+option)]['commands'])
                request.setEnable(commands[str('set_'+option)]['enable'])
                request.setConfigure(commands[str('set_'+option)]['configure'])

                for p in request['commands']:
                    if 'param' in p:
                        if p["type"]:
                            if p["type"] == "interface":
                                p["command"] = p["command"] + interface.strip()
                            elif p["type"] == params.option.strip():
                                p["command"] = p["command"] + new_param.strip()
                            else:
                                p["command"] = p["command"] + new_param.strip()
                        #print p["command"]

                    #set config request to generate input.json file
                config.set_request(request)

                #write config model into input.json file
                self.ci.write_source_file(config, Resources.ci_source, 'JSON')

                #call communication interface script and gather response - RPC
                print "Executing device commands please wait..."
                resp = json.loads(
                    unicode(
                        self.ci.call_communication_interface(Resources.ci_source)
                    )
                    .replace('\n',''),
                    encoding='utf-8'
                )

                #remove input.json
                os.remove(Resources.ci_source)

                #check if rpc is responded
                if resp:
                    #check if wap is connected and returned with success status message 110
                    if resp['status'] == 110:
                        cmd = SQL.SQL_UPDATE_DEVICE_CONFIG % {
                            'key': option,
                            'value': new_param,
                            'modified': self.now,
                            'id': int(device.get_id())
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
        except Exception as e:
            print e.message
            pass

    def unset(self, params):
        """
            This methods handle options and connect throug device by given name
        :param params:
        """
        from src.controller.ConfigMethods import ConfigMethods
        device = Device()
        config = device.get_config()
        request = config.get_request()
        commands = request.getCommands()
        config = Config()
        configMethods = ConfigMethods(config, params)
        try:
            if params.option:
                option = params.option.strip()
            else:
                print Language.MSG_ERR_EMPTY_OPTION.format('device')
                option = raw_input("Please enter an option to be unset:")

            if params.id:
                device.set_id(params.id.strip())
            else:
                print Language.MSG_ERR_EMPTY_ID.format('device')
                device.set_id(raw_input("Please enter an id to define the device:"))

            if device.get_id():
                #gather device detail
                rsetDevice = self.read(device.get_id())
                dataDevice = dict(map(list, zip(rsetDevice['fields'], rsetDevice['results'])))
                dataDevice["Add Date"] = dataDevice["Add Date"].strftime(Resources.time_format)
                dataDevice["Last Modified"] = dataDevice["Last Modified"].strftime(Resources.time_format)
                device.update(dataDevice)

                rsetConfig = configMethods.read(dataDevice["Configuration"])
                dataConfig = dict(map(list, zip(rsetConfig['fields'], rsetConfig['results'])))
                dataConfig["Add Date"] = dataConfig["Add Date"].strftime(Resources.time_format)
                dataConfig["Last Modified"] = dataConfig["Last Modified"].strftime(Resources.time_format)
                config.update(dataConfig)

                #set device config by updated config
                device.set_config(config)

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

                #set request
                print "Request generating..."

                #gather interface and params
                print "Your command(s) will be executing... Please enter required command params below:\n"
                interface = raw_input("Enter parameter for interface of required device:")
                new_param = raw_input("Enter parameter for %(type)s this command of device:" % {'type': params.option})


                if str('unset_'+option) in commands:
                    request.setCommands(commands[str('unset_'+option)]['commands'])
                    request.setEnable(commands[str('unset_'+option)]['enable'])
                    request.setConfigure(commands[str('unset_'+option)]['configure'])

                    for p in request['commands']:
                        if 'param' in p:
                            if p["type"]:
                                if p["type"] == "interface":
                                    p["command"] = p["command"] + interface.strip()
                                elif p["type"] == params.option.strip():
                                    p["command"] = p["command"] + new_param.strip()
                                else:
                                    p["command"] = p["command"] + new_param.strip()
                                    #print p["command"]

                                #set config request to generate input.json file
                    config.set_request(request)

                    #write config model into input.json file
                    self.ci.write_source_file(config, Resources.ci_source, 'JSON')

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
                            cmd = SQL.SQL_UPDATE_DEVICE_CONFIG % {
                                'key': option,
                                'value': '',
                                'modified': self.now,
                                'id': int(config.get_id())
                            }

                            #insert updated config and gather inserted record id
                            self.db.update(cmd)
                            #os.remove(Resources.ci_source)
                        else:
                            print Language.MSG_ERR_COMM_INTERFACE_CONNECTED_BUT_FAILED.format(resp['message'])
                            pass
                    else:
                        print Language.MSG_ERR_COMM_INTERFACE_FAILED
                        pass
                else:
                    print "No such an unset command found on config file for given %(option)s" % {'option': params.option}
                    pass
        except Exception as e:
            print e.message
            pass

    # this method works fine do not touch it!!!
    def show(self, params):
        from src.controller.ConfigMethods import ConfigMethods
        device = Device()
        config = Config()
        request = config.get_request()
        commands = request.getCommands()
        configMethods = ConfigMethods(config, params)
        try:
            if params.option:
                option = params.option.strip()
            else:
                print Language.MSG_ERR_EMPTY_OPTION.format('device')
                option = raw_input("Please enter an option you would like to set:")

            if params.id:
                device.set_id(params.id.strip())
            else:
                print Language.MSG_ERR_EMPTY_ID.format('device')
                device.set_id(raw_input("Please enter an ID you would like to set:"))

            if device.get_id():
                #gather device detail
                rsetDevice = self.read(device.get_id())
                dataDevice = dict(map(list, zip(rsetDevice['fields'], rsetDevice['results'])))
                dataDevice["Add Date"] = dataDevice["Add Date"].strftime(Resources.time_format)
                dataDevice["Last Modified"] = dataDevice["Last Modified"].strftime(Resources.time_format)
                device.update(dataDevice)

                rsetConfig = configMethods.read(dataDevice["Configuration"])
                dataConfig = dict(map(list, zip(rsetConfig['fields'], rsetConfig['results'])))
                dataConfig["Add Date"] = dataConfig["Add Date"].strftime(Resources.time_format)
                dataConfig["Last Modified"] = dataConfig["Last Modified"].strftime(Resources.time_format)
                config.update(dataConfig)

                #set device config by updated config
                device.set_config(config)

                #gather commands config file content
                config_source = self.ci.get_source_config(Resources.cfg_device_resource)

                #check config source and load inside data
                if config_source:
                    #turn into dictionary from json
                    commands = json.loads(unicode(config_source))

                #set request
                print "Request generating..."

                request.setCommands(commands[str('show_'+option)]['commands'])
                request.setEnable(commands[str('show_'+option)]['enable'])
                request.setConfigure(commands[str('show_'+option)]['configure'])

                #set config request to generate input.json file
                config.set_request(request)

                #write config model into input.json file
                self.ci.write_source_file(config, Resources.ci_source, 'JSON')

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
                        if not resp['message'] and resp['message'] is None:
                            print "There is no active %(option)s" % {'option':option}
                        elif resp['message'] or resp['message'] is not None:
                            print resp['message']
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

    def group_set(self, config, params):
        """
        Group set makes users to set handle group operations for set command. It can be done by user such as ssid,
        channel, associations, etc.

        Group set moderated by @class Main and @method set by seperating type arguments such as group.
        Sample usage to reach this method is below:
        $ set -t group -o [OPTION] -i [id]

        :param config:
        :param params:
        """
        config_source = self.ci.get_source_config(Resources.cfg_device_resource)

        #check config source and load inside data
        if config_source:
            try:
                #turn into dictionary from json
                commands = json.loads(unicode(config_source))
            except Exception as e:
                print e.message
                pass

        # get/set option
        option = params.option.strip()

        # get interface and param
        interface = params.interface.strip()
        new_param = params.param.strip()

        #set request
        request = config.get_request()
        
        #execute pre requested commands if exists
        if 'pre' in commands[str('set_'+option)]:
            #get existing records from database and unset them from device
            pre = commands[str('set_'+option)]['pre']
            #print "Prerequesting command(s) being executed. Please wait...\n"
            request.setCommands(commands[str(pre + '_'+ option)]['commands'])
            request.setEnable(commands[str(pre + '_'+ option)]['enable'])
            request.setConfigure(commands[str(pre + '_'+ option)]['configure'])

            for p in request['commands']:
                if 'param' in p:
                    #new param has been approved??
                    if p["type"]:
                        if p["type"] == "interface":
                            p["command"] = p["command"] + interface
                        elif p["type"] == option:
                            p["command"] = p["command"] + config[option]
                        else:
                            p["command"] = p["command"] + config[option]
                            #print p["command"]

            #set config request to generate input.json file
            config.set_request(request)

            #write config model into input.json file
            self.ci.write_source_file(config, Resources.ci_source, 'JSON')

            #call communication interface script and gather response - RPC
            #print "Executing device commands please wait..."
            resp = json.loads(
                unicode(
                    self.ci.call_communication_interface(Resources.ci_source)
                )
                .replace('\n',''),
                encoding='utf-8'
            )

            #remove input.json
            #os.remove(Resources.ci_source)

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
                        p["command"] = p["command"] + interface.strip()
                    elif p["type"] == params.option.strip():
                        p["command"] = p["command"] + new_param.strip()
                    else:
                        p["command"] = p["command"] + new_param.strip()
                        #print p["command"]

                        #set config request to generate input.json file
        config.set_request(request)

        #write config model into input.json file
        source_input = Resources.input_source % { 'file': config['Device']}
        self.ci.write_source_file(config,source_input, 'JSON')

        #call communication interface script and gather response - RPC
        #print "Executing device commands please wait..."
        resp = json.loads(
            unicode(
                self.ci.call_communication_interface(source_input)
            )
            .replace('\n',''),
            encoding='utf-8'
        )

        #remove source input
        os.remove(source_input)

        #check if rpc is responded
        if resp:
            #check if wap is connected and returned with success status message 110
            if resp['status'] == 110:
                cmd = SQL.SQL_UPDATE_DEVICE_CONFIG % {
                    'key': option,
                    'value': new_param,
                    'modified': self.now,
                    'id': int(config['Device'])
                }

                #insert updated config and gather inserted record id
                if self.db.update(cmd):
                    #resp['message']
                    os.remove(Resources.ci_source)
                    print '\t'+config['ip']+'\t\tstatus => OK'
                else:
                    self.group_set(config, params)
                return True
            else:
                print '\t'+config['ip']+'\t\tstatus => FAILED'
                raise Exception(
                        Language.MSG_ERR_COMM_INTERFACE_CONNECTED_BUT_FAILED.format(resp['message'])
                )
        else:
            raise Exception(Language.MSG_ERR_COMM_INTERFACE_FAILED)