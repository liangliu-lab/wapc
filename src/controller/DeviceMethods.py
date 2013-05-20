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

import json
import os
import threading
from time import strftime, gmtime
from src.cli.CommunicationInterface import CommunicationInterface
from src.resources.SQL import SQL
from src.helpers.Utils import Utils
from src.database.Database import Database
from src.language.Language import Language
from src.model.Device import Device
from src.model.Config import Config
from src.model.Request import Request
from src.resources.Resources import Resources

__author__ = 'fatih'


class DeviceMethods(threading.Thread):
    """
        DeviceMethods class includes device oriented methods such CRUD
        operations.

        Methods covered by DeviceMethods and other controller methods in other
        might be similar each other but in deep they have their own custom
        attributes and variables to determine each process is focused to the
        target.
    """

    def __init__(self, params):
        """
        Constructor for DeviceMethods
        """
        super(DeviceMethods, self).__init__()
        self.utils = Utils()
        self.database = Database(Resources.cfg_section_master_db)
        self.log_database = Database(Resources.cfg_section_log_db)
        self.communication_interface = CommunicationInterface()
        self.script = Resources.ci_script
        self.cfg_device = Resources.cfg_device_resource
        self.now = strftime(Resources.time_format, gmtime())
        self.params = params

    def create(self, params):
        """
        Create method aims to create a new device insert it into database and
        apply the config regarding given brand, model and firmware.

        Create method is called by Main.add method by given type. Type should be
        provided as 'device'. Also when adding a new device arguments listed
        below have to be provided:

        <h3>Usage: $ add [OPTIONS]</h3>
        Add device, group, vlan, config etc with given parameters
        <ul>
        <li>[-t],[--type] Define type device, group, vlan, config</li>
        <li>[-I],[--ip] Use this params when adding some new variables which 
        needs an ip such as device, config, etc.</li>
        <li>[-n],[--name] To set a name to related type variable</li>
        <li>[-b],[--brand] To set device brand to relate with its model and/or 
        firmware</li>
        <li>[-m],[--model] To set device model to relate with its config file
        </li>
        <li>[-F],[--firmware] To set device firmware to relate with its config
        file</li>
        <li>[-R],[--relation] To set device relation one of MASTER of SLAVE</li>
        <li>[-D],[--description] To set a description to related type variable
        </li>
        <li>[-u],[--username] Provide a username which will be used to connect
        device</li>
        <li>[-p],[--password] Provide a password which will be used to connect 
        and configure device</li>
        </ul>

        If there is no parameter provided every required parameter will be
        gathered by asking the user to provide every single parameter.

        @param params
        """
        device = Device()
        config = device.get_config()
        request = config.get_request()

        try:
            #===================================
            # check namespace variables if set then set them
            # into device model variables
            #===================================

            # set device ip to connect to the device
            if params.ip:
                device.set_ip(params.ip.strip())
            else:
                print Language.MSG_ERR_EMPTY_IP.format('device')
                new_ip = raw_input("Please enter an IP address:")
                if device.set_ip(new_ip):
                    pass
                else:
                    print "The IP address you provide is not in a valid format"
                    print "Process will start over"
                    raise BaseException(
                        "The IP address you provide is not in a valid format"
                    )

            # set device name to connect to the device
            if params.name:
                device.set_name(params.name.strip())
            else:
                print Language.MSG_ERR_EMPTY_NAME.format('device')
                device.set_name(raw_input("Please enter an nick name:").strip())

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
                device.set_username(
                    raw_input("Please enter an username:").strip())

            # set device password to connect to the device
            if params.password:
                device.set_password(params.password.strip())
            else:
                print Language.MSG_ERR_EMPTY_PASSWORD.format('device')
                device.set_password(
                    raw_input("Please enter a password:").strip())

            # define config file path to initial a new device
            # ==============================================
            # concluded path should be like this at the end:
            # config/[brand]/[model]/[firmware]/[relation]-config.conf
            # if no params provided at least brand required and
            # the final path should be below:
            # config/[brand]/default/default/slave-config.conf
            # ==============================================
            path = None
            if params.brand:
                device.set_device_brand(str(params.brand.strip()).lower())
            else:
                print (
                    "It must be provided at least brand to identify "
                    "which device you would like to add to the inventory. "
                    "See help below:\n"
                    + Language.MSG_ADD_BRAND_HELP +
                    "\nPlease use 'help' command to see detailed usage."
                )
                device.set_device_brand(
                    raw_input("Please enter a brand:").lower()
                )

            if params.model:
                device.set_model(str(params.model.strip()).lower())
                if params.firmware:
                    device.set_firmware(
                        str(params.firmware.strip()).lower())
                    path = "%s/%s/%s".format(device.get_brand(),
                                             device.get_model(),
                                             device.get_firmware())
                else:
                    path = "%s/%s/default".format(device.get_brand(),
                                                  device.get_model())
            else:
                path = device.get_brand() + "/default/default"

            if params.relation:
                device.set_relation(str(params.relation.strip()).lower())
            else:
                print "You did not provide a relation such as " \
                      "one of 'master' or 'slave'. " \
                      "Therefore, the default value is set to 'slave'."

            #gather commands config
            # config_source = self.ci.get_source_config(Resources.ci_config)
            if path and device.get_relation():
                # set default config file path
                config_source_file = Resources.device_initial_config % \
                                     {'path': path,
                                      'relation': device.get_relation()}

                # get default config file content
                config_source = self.communication_interface.get_source_config(
                    config_source_file)

                # replace ip address, ssid and channel in file content
                config_source = config_source \
                    .replace('##ip##', device.get_ip())
                config_source = config_source.replace('##ssid##',
                                                      config.get_ssid())
                config_source = config_source.replace('##channel##',
                                                      str(config.get_channel()))

                # write new content into default config file
                tftp_target = Resources.device_tftp_path % \
                              {'relation': device.get_relation()}
                self.communication_interface.write_source_file(
                    config_source, tftp_target, 'RAW')
            else:
                raise Exception(
                    "Device config path could not be found or not correctly "
                    "configured please check given parameters" \
                    "then try again. Here is recent path: " +
                    Resources.device_initial_config %
                    {'path': path, 'relation': device.get_relation()})

            # get default config object into a dict
            if config_source:
                # replace recent ip in config file and generate commands
                commands = json.loads(unicode(
                    self.communication_interface.get_source_config(
                        Resources.device_load_command)))
                commands['commands'][0]['command'] = \
                    commands['commands'][0]['command'] % \
                    {'file': Resources.device_tftp_file %
                             {'relation': device.get_relation()}
                    }
                #commands = json.loads(unicode(config_source))
            else:
                raise IOError(Language.MSG_ERR_FILE_READ %
                              {
                                  'error': 'IOError',
                                  'file': Resources.device_load_command
                              })

            #set config parameters to relate with device
            config.set_name(device.get_name())
            config.set_username(device.get_username())
            config.set_password(device.get_password())
            config.set_enable_password(config.get_password())
            config.set_transport_protocol(
                device.get_config().get_transport_protocol())
            config.set_personality(device.get_config().get_personality())

            #set request
            request.set_enable(True)
            request.set_configure(False)

            #get device recent config
            request.set_commands(commands['commands'])

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
            # ======================================
            # Write config object into file with write_source_file method
            # with parameter source and source type
            # Source type can be JSON or RAW or XML
            # ======================================
            # utils.get_request_config()
            target_file = self.utils.get_request_config(device, config)
            #self.communication_interface.write_source_file(
            #    config, Resources.ci_source, 'JSON')

            #call communication interface script and gather response - RPC
            #print Language.MSG_EXE_REQUEST
            resp = json.loads(
                unicode(
                    self.communication_interface.
                    call_communication_interface(target_file)
                )
                .replace('\n', ''),
                encoding='utf-8'
            )
            #remove input.json
            os.remove(target_file)

            #check if rpc is responded
            if resp:
                #check if wap is connected and returned with success
                #status message 110
                if resp['status'] == 110:
                    #insert new device to the database
                    cmd = SQL.SQL_INSERT_DEVICE % {
                        "name": device.get_name(),
                        "username": device.get_username(),
                        "password": device.get_password(),
                        "desc": device.get_description(),
                        "ip": device.get_ip(),
                        "brand": device.get_brand(),
                        "model": device.get_model(),
                        "firmware": device.get_firmware(),
                        "relation": device.get_relation(),
                        "date_added": self.now,
                        "date_modified": self.now
                    }

                    #get inserted device id and inform user
                    device_id = self.database.insert(cmd)

                    if device_id[0]:
                        #write recent config into backup file
                        self.communication_interface.backup(
                            config_source,
                            config.get_name(),
                            self.now,
                            'RAW'
                        )
                        print Language.MSG_STATUS_ADD_SUCCESS % \
                              {
                                  'type': 'device',
                                  'id': device_id[0],
                                  'name': device.get_name()
                              }

                    cmd = SQL.SQL_INSERT_CONFIG % {
                        "name": config.get_name(),
                        "description": config.get_description(),
                        "radius_config_id": config.get_radius(),
                        "ssid": config.get_ssid(),
                        "vlan_id": config.get_vlan(),
                        "channel": config.get_channel(),
                        "maxclient": config.get_maxclient(),
                        "username": config.get_username(),
                        "password": config.get_password(),
                        "enable_password": config.get_enable_password(),
                        "transport_protocol": config.get_transport_protocol(),
                        "personality": config.get_personality(),
                        "belong_to": int(device_id[0]),
                        "date_added": self.now,
                        "date_modified": self.now
                    }

                    # insert new config record to database then get its row id
                    cid = self.database.insert(cmd)

                    if cid:
                        device.set_config_id(cid[0])
                        print Language.MSG_STATUS_ADD_SUCCESS % \
                              {
                                  'type': 'config',
                                  'id': cid[0],
                                  'name': config.get_name()
                              }
                else:
                    print Language.MSG_ERR_COMM_INTERFACE_CONNECTED_BUT_FAILED. \
                        format(resp['message'])
            else:
                print Language.MSG_ERR_COMM_INTERFACE_FAILED
        except BaseException as exception:
            raise BaseException("An error occurred: %s" % {exception.message})

    def read(self, cid):
        """

        :param id:
        """
        try:
            #check namespace variables if set

            #moderate type value to determine the statement
            cmd = SQL.SQL_SELECT_DEVICE % {'id': int(cid)}
            fields, results = self.database.select(cmd)
            if fields and results:
                try:
                    rset = {"fields": fields,
                            "results": [list(f) for f in results][0]}
                    return rset
                except BufferError as exception:
                    print exception.message
            else:
                raise self.database.DatabaseError(
                    Language.MSG_ERR_GENERIC.format(
                        self.utils.get_line(),
                        Language.MSG_ERR_DATABASE_NORECORD))
        except BaseException as exception:
            raise BaseException("An error occurred: %s" % {exception.message})

    def update(self, params):
        """
        Update methods certainly moderated by $ edit [OPTIONS] command by CLI.

        This methods only inherit update database records by no touching
        physical device config.

        @params params comes from main class
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

                self.database.update(cmd)
            else:
                raise Exception(
                    "Error occured while getting required parameters "
                    "device 'id', option, and param")
        except BaseException as exception:
            raise exception.message

    # this method works fine do not touch it!!!
    def set(self, params):
        """
        This methods handle options and connect through device by given name

        Params contains a command option either one of set or unset. Regarding
        this params.command option method decides what operation will be
        implemented.

        @param params
        """
        from src.controller.ConfigMethods import ConfigMethods

        device = Device()
        config = Config()
        request = config.get_request()
        commands = request.get_commands()
        config_methods = ConfigMethods(config, params)
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
                device.set_id(
                    raw_input("Please enter id for device will be set:"))

            if device.get_id():
                #gather device detail
                rset_device = self.read(device.get_id())
                data_device = self.utils.wellform_dict(
                    rset_device, 'fields', 'results')
                data_device = self.utils.fix_date(data_device)
                device.update(data_device)

                rset_config = config_methods.read(data_device["Configuration"])
                data_config = self.utils.wellform_dict(
                    rset_config, 'fields', 'results')
                config.update(data_config)

                #set device config by updated config
                device.set_config(config)

                #gather commands config file content
                config_source = self.communication_interface \
                    .get_source_config(Resources.cfg_device_resource)

                #check config source and load inside data
                if config_source:
                    #turn into dictionary from json
                    commands = json.loads(unicode(config_source))

                if str(params.command + '_' + option) not in commands:
                    raise BaseException(
                        "There is no command found on your device "
                        "commands file '%s'" % option
                    )

                #set request
                print "Request generating..."

                #gather interface and params
                print "Your command(s) will be executing... " \
                      "Please enter required command params below:\n"
                interface = raw_input("Enter parameter for interface of "
                                      "required device:")
                new_param = raw_input("Enter parameter for %(type)s this "
                                      "command of device:" %
                                      {'type': option})

                # set new value to given variable where option is its attribute
                #config[option] = new_param

                if params.command is "set":
                    self.execute_precommand(device, commands, config, interface,
                                            request, params, option)

                # set config option value
                config[option] = new_param.strip()

                request.set_commands(commands[str(params.command + '_' +
                                                  option)]['commands'])
                request.set_enable(commands[str(params.command + '_' +
                                                option)]['enable'])
                request.set_configure(
                    commands[str(params.command + '_' + option)]['configure'])

                for command in request['commands']:
                    if 'param' in command:
                        if command["type"]:
                            if command["type"] == "interface":
                                command["command"] += interface.strip()
                            elif command["type"] != option:
                                command["command"] += config[command["type"]]
                            elif command["type"] == option:
                                command["command"] += new_param.strip()
                            else:
                                command["command"] += new_param.strip()
                                #print p["command"]

                                #set config request to generate input.json file
                config.set_request(request)

                #write config model into input.json file
                target_file = self.utils.get_request_config(device, config)
                #self.communication_interface \
                #    .write_source_file(config, Resources.ci_source, 'JSON')

                #call communication interface script and gather response - RPC
                print "Executing device commands please wait..."
                resp = json.loads(
                    unicode(
                        self.communication_interface
                        .call_communication_interface(target_file)
                    )
                    .replace('\n', ''),
                    encoding='utf-8'
                )

                #remove input.json
                os.remove(target_file)

                #check if rpc is responded
                if resp:
                    #check if wap is connected and returned with success
                    # status message 110
                    if resp['status'] == 110:
                        if params.command is "set":
                            cmd = SQL.SQL_UPDATE_DEVICE_CONFIG % {
                                'key': option,
                                'value': new_param,
                                'modified': self.now,
                                'id': int(device.get_id())
                            }
                        elif params.command is "unset":
                            cmd = SQL.SQL_UPDATE_DEVICE_CONFIG % {
                                'key': option,
                                'value': "",
                                'modified': self.now,
                                'id': int(device.get_id())
                            }

                        #insert updated config and gather inserted record id
                        self.database.update(cmd)
                    else:
                        print Language \
                            .MSG_ERR_COMM_INTERFACE_CONNECTED_BUT_FAILED \
                            .format(resp['message'])
                else:
                    print Language.MSG_ERR_COMM_INTERFACE_FAILED
        except BaseException as exception:
            raise exception.message

    # this method works fine do not touch it!!!
    def show(self, params):
        """
        Show methods submit returns where sh commands came from.

        Show methods gathers parameter, read commands file regarding device
        brand, model etc and then generate a JSON file and execute this file
        with CommunicationInterface

        @rtype : object
        @param params
        """
        from src.controller.ConfigMethods import ConfigMethods

        device = Device()
        config = Config()
        request = config.get_request()
        commands = request.get_commands()
        config_methods = ConfigMethods(config, params)
        try:
            if params.id:
                device.set_id(params.id.strip())
            else:
                print Language.MSG_ERR_EMPTY_ID.format('device')
                device.set_id(raw_input(Language.MSG_INPUT_PARAM_OPTION %
                                        {'param': 'ID'}))
            if params.option:
                option = params.option.strip()
            else:
                print Language.MSG_ERR_EMPTY_OPTION
                option = raw_input()
            if device.get_id():
                #gather device detail
                rset_device = self.read(device.get_id())
                data_device = self.utils.wellform_dict(
                    rset_device, 'fields', 'results')
                data_device = self.utils.fix_date(data_device)
                device.update(data_device)

                rset_config = config_methods.read(data_device["Configuration"])
                data_config = self.utils.wellform_dict(
                    rset_config, 'fields', 'results')

                data_config = self.utils.fix_date(data_config)
                config.update(data_config)

                #set device config by updated config
                device.set_config(config)

                #gather commands config file content
                config_source = self.communication_interface \
                    .get_source_config(Resources.cfg_device_resource)

                #check config source and load inside data
                if config_source:
                    #turn into dictionary from json
                    commands = json.loads(unicode(config_source))

                #set request
                print "Request generating..."

                if not commands[str('show_' + option)]:
                    raise BaseException(
                        "There is no command found on your device "
                        "commands file '%s'" % option
                    )

                request.set_commands(
                    commands[str('show_' + option)]['commands'])
                request.set_enable(
                    commands[str('show_' + option)]['enable'])
                request.set_configure(
                    commands[str('show_' + option)]['configure'])

                #set config request to generate input.json file
                config.set_request(request)

                target_file = self.utils.get_request_config(device, config)
                #self.communication_interface.write_source_file(
                #    config, Resources.ci_source, 'JSON')

                #call communication interface script and gather response - RPC
                print Language.MSG_EXE_REQUEST
                resp = json.loads(
                    unicode(
                        self.communication_interface.
                        call_communication_interface(target_file)
                    )
                    .replace('\n', ''),
                    encoding='utf-8'
                )
                #remove input.json
                os.remove(target_file)

                #check if rpc is responded
                response = None
                if resp:
                    # check if wap is connected and returned with success
                    # status message 110
                    if resp['status'] == 110:
                        if not resp['message'] and resp['message'] is None:
                            response = "There is no active %(option)s" \
                                       % {'option': option}
                        elif resp['message'] or resp['message'] is not None:
                            response = resp['message']
                            #os.remove(Resources.ci_source)
                    else:
                        response = Language \
                            .MSG_ERR_COMM_INTERFACE_CONNECTED_BUT_FAILED \
                            .format(resp['message'])
                else:
                    response = Language.MSG_ERR_COMM_INTERFACE_FAILED
                return response
        except BaseException as exception:
            raise BaseException("An error occurred: %s" % {exception.message})

    def group(self, params, queue, config=Config()):
        """
        Group set makes users to set handle group operations for set command.
        It can be done by user such as ssid, channel, associations, etc.

        Group set moderated by @class Main and @method set by separating type
        arguments such as group.

        Sample usage to reach this method is below:
        $ set -t group -o [OPTION] -i [id]

        @param config
        @param params
        """
        try:
            config_source = self.communication_interface \
                .get_source_config(Resources.cfg_device_resource)
            #turn into dictionary from json
            commands = json.loads(unicode(config_source))
            params.ssid = self.database.get('ssid', config["Device"])
            # get/set option
            if params.option:
                option = params.option.strip()

            # get interface and param
            interface = params.interface.strip()
            if params.param:
                new_param = params.param.strip()

            # check if command exist in command list
            if str(params.command + '_' + option) not in commands:
                raise BaseException(
                    "Submitted command is not in the config json!"
                )

            #set request
            request = Request()

            #execute pre requested commands if exists
            if 'pre' in commands[str(params.command + '_' + option)]:
                #get existing records from database and unset them from device
                pre = commands[str(params.command + '_' + option)]['pre']
                request.set_commands(
                    commands[str(pre + '_' + option)]['commands'])
                request.set_enable(
                    commands[str(pre + '_' + option)]['enable'])
                request.set_configure(
                    commands[str(pre + '_' + option)]['configure'])

                for command in request['commands']:
                    if 'param' in command:
                        #new param has been approved??
                        if command["type"]:
                            if command["type"] == "interface":
                                command["command"] += interface
                            elif command["type"] == option:
                                command["command"] += config[option]
                            else:
                                command["command"] += config[option]
                                #print p["command"]

                #set config request to generate input.json file
                config["request"] = request

                #write config model into input.json file
                device = Device()
                device.set_id(config["Device"])
                target_file = self.utils.get_request_config(device, config)
                #self.communication_interface \
                #    .write_source_file(config, Resources.ci_source, 'JSON')

                #call communication interface script and gather response - RPC
                #print "Executing device commands please wait..."
                resp = json.loads(
                    unicode(
                        self.communication_interface
                        .call_communication_interface(target_file)
                    )
                    .replace('\n', ''),
                    encoding='utf-8'
                )

                #remove input.json
                os.remove(target_file)

                # check if rpc is responded and shows that pre-request command
                # successfully executed
                if resp:
                    pass
                    # check if wap is connected and returned with success status
                    # message 110
                    #    if resp['status'] == 110:
                    #        print "Pre-request command(s) successfully executed"

            request.set_commands(
                commands[
                    str(params.command + '_' + option)
                ]['commands'])
            request.set_enable(
                commands[
                    str(params.command + '_' + option)
                ]['enable'])
            request.set_configure(
                commands[
                    str(params.command + '_' + option)
                ]['configure'])

            if params.param:
                for command in request['commands']:
                    if 'param' in command:
                        if command["type"]:
                            if command["type"] == "interface":
                                command["command"] += interface.strip()
                            elif command["type"] == "ssid":
                                command["command"] += params.ssid.strip()
                            elif command["type"] == params.option.strip():
                                command["command"] += new_param.strip()
                            else:
                                command["command"] += new_param.strip()
                                #print p["command"]

                                #set config request to generate input.json file
            config["request"] = request

            #write config model into input.json file
            device = Device()
            device.set_ip(config["ip"])
            device.set_id(config["Device"])
            input_source = self.utils.get_request_config(device, config)

            #call communication interface script and gather response - RPC
            #print "Executing device commands please wait..."
            resp = json.loads(
                unicode(
                    self.communication_interface
                    .call_communication_interface(input_source)
                )
                .replace('\n', ''),
                encoding='utf-8'
            )

            #remove source input
            os.remove(input_source)

            #check if rpc is responded
            if resp:
                # check if wap is connected and returned with success status

                # message 110
                if resp['status'] == 110:
                    #insert updated config and gather inserted record id
                    if params.command == "set":
                        cmd = SQL.SQL_UPDATE_DEVICE_CONFIG % {
                            'key': option,
                            'value': new_param,
                            'modified': self.now,
                            'id': int(config['Device'])
                        }
                        self.database.update(cmd)
                    elif params.command == "unset":
                        cmd = SQL.SQL_UPDATE_DEVICE_CONFIG % {
                            'key': option,
                            'value': "",
                            'modified': self.now,
                            'id': int(config['Device'])
                        }
                        self.database.update(cmd)

                    response = (config["Device"],
                                config["Device Name"],
                                config["ip"],
                                option,
                                "Connected",
                                resp['message'])
                else:
                    response = (config["Device"],
                                config["Device Name"],
                                config["ip"],
                                option,
                                "Not Connected",
                                resp['message'])
                    #self.group(params, queue, config)
                queue.put(response)
            else:
                raise BaseException(
                    Language.MSG_ERR_COMM_INTERFACE_FAILED %
                    {
                        "line": self.utils.get_line(),
                        "exception": "[No response has been returned]"
                    }
                )
        except BaseException as exception:
            raise BaseException("An error occurred: %s" % {exception.message})

    def execute_precommand(self, device,
                           commands, config,
                           interface, request,
                           params, option):
        """
        Execute pre-requested device commands
        @param device
        @param commands
        @param config
        @param interface
        @param request
        @param params
        @param option
        @return
        """
        try:
            if 'pre' in commands[str(params.command + '_' + option)]:
                pre = commands[str(params.command + '_' + option)]['pre']
                request.set_commands(
                    commands[str(pre + '_' + option)]['commands'])
                request.set_enable(
                    commands[str(pre + '_' + option)]['enable'])
                request.set_configure(
                    commands[str(pre + '_' + option)]['configure'])

                for command in request['commands']:
                    if 'param' in command:
                        #new param has been approved??
                        if command["type"]:
                            if command["type"] == "interface":
                                command["command"] += interface.strip()
                            elif command["type"] == params.option.strip():
                                command["command"] += config.get_ssid()
                            else:
                                command["command"] += config.get_ssid()
                                #print p["command"]

                #set config request to generate input.json file
                config.set_request(request)

                #write config model into input.json file
                target_file = self.utils.get_request_config(device, config)
                #self.communication_interface.write_source_file(
                #    config, Resources.ci_source, 'JSON')

                #call communication interface script and gather
                # response - RPC
                #print "Executing device commands please wait..."
                resp = json.loads(
                    unicode(
                        self.communication_interface
                        .call_communication_interface(target_file)
                    )
                    .replace('\n', ''),
                    encoding='utf-8'
                )

                #remove input.json
                os.remove(target_file)

                # check if rpc is responded and shows that pre-request
                # command
                # successfully executed
                if resp:
                    #check if wap is connected and returned with success
                    # status message 110
                    if resp['status'] == 110:
                        #print "Pre-request command(s) successfully executed"
                        pass
        except BaseException as exception:
            raise BaseException("An error occurred: %s" % {exception.message})

    def get_device_list(self):
        """
        This method gather all devices from inventory and return a list
        @return:
        """
        cmd = SQL.SQL_SELECT_DEVICE_ALL
        fields, results = self.database.select(cmd)
        del fields
        return results
