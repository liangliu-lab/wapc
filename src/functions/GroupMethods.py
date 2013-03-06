# coding=utf-8
from Queue import Empty
from time import strftime, gmtime
from src.config.__sql__ import SQL
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
                group.setName(params.name.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_NAME.format('group')

            if params.description:
                group.setDescription(params.name.rstrip().lstrip())
            else:
                print Language.MSG_ERR_EMPTY_NAME.format('group')

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
            if gID is Empty:
                print Language.MSG_ERR_DATABASE_ERROR.format(self.utils.get_line(), 'inserting new group', gID[0])
            else:
                print Language.MSG_ADD_NEW.format('group', gID[0], group.getName())
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

    def update(self, params):
        """
        :param params:
        """
        group = Group()
        try:
            if params.id:
                did = params.id.rstrip().lstrip()
                rset = self.read(did)
                data = dict(map(list, zip(rset['fields'], rset['results'])))

                if params.name:
                    group.setName(params.name.rstrip().lstrip())
                else:
                    group.setName(data["name"])
                if params.description:
                    group.setDescription(params.description.rstrip().lstrip())
                else:
                    group.setDescription(data["description"])
                if params.config:
                    group.setConfig(params.config.rstrip().lstrip())
                else:
                    group.setConfig(data["config"])

                group.setModified(self.now)

                cmd = SQL.SQL_UPDATE_GROUP % \
                      {
                          "name": group.getName(),
                          "description": group.getDescription(),
                          "config_id": int(group.getConfig()),
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
        :param params:
        """
        # TODO implement group editing one by one device
        # TODO get all devices under given group by SQL
        # TODO set update every config file belongs to given device

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

            #if params.parameter:
            #    param = params.parameter.rstrip().lstrip()
            #else:
            #    print Language.MSG_ERR_EMPTY_PARAMETER.format('device')

            if device.getID():# and param:
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

                config.setName(device.getName())
                #if option == "ssid":
                #    config.setSSID(param)
                #elif option == "vlan":
                #    config.setVLAN(param)

                config.setIP(device.getIP())
                config.setUsername(device.getUsername())
                config.setPassword(device.getPassword())
                config.setEnablePassword(dataConfig["enable_password"])
                config.setTProtocol(dataConfig["transport_protocol"])
                config.setPersonality(dataConfig["personality"])

                #set request
                #get device recent config
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
                            #p["command"] = p["command"] + " " + self.utils.validate(param, 'name')
                            #new param has been approved??
                            if p["type"]:
                                if p["type"] == "interface":
                                    p["command"] = p["command"] + interface.rstrip().lstrip()
                                elif p["type"] == params.option.rstrip().lstrip():
                                    p["command"] = p["command"] + new_param.rstrip().lstrip()
                                else:
                                    p["command"] = p["command"] + new_param.rstrip().lstrip()
                            print p["command"]

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
                        #p["command"] = p["command"] + " " + self.utils.validate(param, 'name')
                        #new param has been approved??
                        if p["type"]:
                            if p["type"] == "interface":
                                p["command"] = p["command"] + interface.rstrip().lstrip()
                            elif p["type"] == params.option.rstrip().lstrip():
                                p["command"] = p["command"] + new_param.rstrip().lstrip()
                            else:
                                p["command"] = p["command"] + new_param.rstrip().lstrip()
                        print p["command"]

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
                        configMethods.update(params)
                        self.update(params)
                        # cmd = SQL.SQL_INSERT_CONFIG.format(
                        #     config.getName(),
                        #     config.getDescription(),
                        #     config.getIP(),
                        #     config.getRadiusID(),
                        #     config.getSSID(),
                        #     config.getVLAN(),
                        #     config.getChannel(),
                        #     config.getChannelFreq(),
                        #     self.now,
                        #     self.now
                        # )
                        #
                        # #insert new config and gather inserted record id
                        # cid = self.db.insert(cmd)
                        # if cid:
                        #     self.device.setConfigID(cid[0])
                        #     print "New configuration generated for the new device with id: %s" % cid[0]
                        # else:
                        #     print Language.MSG_ERR_EMPTY_CONFIG
                        #
                        # #insert new device to the database
                        # cmd = SQL.SQL_INSERT_DEVICE.format(
                        #     self.device.getName(),
                        #     self.device.getDescription(),
                        #     self.device.getIP(),
                        #     cid[0],
                        #     self.device.getUsername(),
                        #     self.device.getPassword(),
                        #     self.now,
                        #     self.now
                        # )
                        #
                        # #get inserted device id and inform user
                        # id = self.db.insert(cmd)
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
            else:
                pass
        except Exception as e:
            print e.message
            pass
