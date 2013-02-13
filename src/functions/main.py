from Queue import Empty
import json
from time import strftime, gmtime
import parser
from src.cli.CommunicationInterface import CommunicationInterface
from src.cli.Utils import Utils
from src.config.__sql__ import SQL
from src.database.db import Database
from src.language.language import Language
from src.model.Commands import Commands
from src.model.Config import Config
from src.model.Device import Device
from src.model.Group import Group
from src.model.Request import Request
from src.model.Response import Response
from src.resources.resources import Resources

__author__ = 'fatih'


class Main(dict):
    """
        Main class includes all base functions of the software
    """

    def __init__(self):
        self.config = Config()
        self.device = Device()
        self.util = Utils()
        self.ci = CommunicationInterface()
        self.db = Database()
        self.now = strftime(Resources.time_format, gmtime())
        self.script = Resources.ci_script
        self.cfg_device = Resources.cfg_device_resource

    def add(self, args):
        """
            Add function to implement a thread at background responds to Web or CLI request
        :param args:
        """
        device = Device()
        config = Config()
        resp = Response()
        request = Request()
        commands = Commands()

        try:
            params = self.util.get_args(args)

            if params:
                if params.type is Empty:
                    print ""
                else:
                    print ""
            else:
                print "error message"
                pass

            #check namespace variables if set
            if params.ip is Empty:
                print Language.MSG_ERR_EMPTY_IP.format('device')
            else:
                device.setIP(params.ip.strip())

            if params.name is Empty:
                print Language.MSG_ERR_EMPTY_NAME.format('device')
            else:
                device.setName(params.name.strip())

            if params.username is Empty:
                print Language.MSG_ERR_EMPTY_USERNAME.format('device')
            else:
                device.setUsername(params.username.strip())

            if params.password is Empty:
                print Language.MSG_ERR_EMPTY_PASSWORD.format('device')
            else:
                device.setPassword(params.password.strip())

            #gather commands config
            config_source = self.ci.get_source_config(Resources.cfg_device_resource) #get config file sort of json

            if config_source:
                try:
                    commands = json.loads(unicode(config_source))
                except Exception as e:
                    print e.message
                    pass

                    #open input file
                    #in_source = self.ci.get_source_config(Resources.ci_source)
                    #if in_source:
                    #read and bind its inside
                    #    try:
                    #        config = json.loads(unicode(in_source))
                    #    except Exception as e:
                    #        print e.message
                    #        pass
                    #else:
                    #read and bind its inside
                    #    config = json.loads(unicode(self.config))

            #set new config params
            config['name'] = device.getName()
            config['ip'] = device.getIP()
            config['username'] = device.getUsername()
            config['password'] = device.getPassword()
            config['transport_protocol'] = device.getConfig().getTProtocol()
            config['enable_password'] = device.getPassword()
            config['personality'] = device.getConfig().getPersonality()

            #set request
            request.setEnable(True)
            request.setConfigure(False)
            #get device recent config
            request.setCommands(commands['show_run']['commands'])

            config['request'] = request.__dict__
            print "Request generating...\n"

            #call communication interface script and gather response - RPC
            try:
                print "Executing device commands please wait..."
                resp = json.loads(unicode(self.ci.call_communication_interface(Resources.ci_source)))
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
                    print "New configuration generated for the new device with id: %s" % cid[0]
                    #cid = str(cid).rfind()
                    #insert new device to the database
                    cmd = SQL.SQL_INSERT_DEVICE.format(
                        device.getName(),
                        device.getIP(),
                        cid[0],
                        device.getUsername(),
                        device.getPassword(),
                        self.now,
                        self.now
                    )

                    #get inserted device id and inform user
                    id = self.db.insert(cmd)
                    if id:
                        #write recent config into backup file
                        self.ci.backup(commands, config.getName(), self.now)
                        print Language.MSG_ADD_NEW.format('device', id[0], device.getName())
                else:
                    print Language.MSG_ERR_COMM_INTERFACE_CONNECTED_BUT_FAILED.format(resp['message'])
            else:
                print Language.MSG_ERR_COMM_INTERFACE_FAILED

        except Exception as e:
            print Language.MSG_ERR_GENERIC.format("34", e.message)
            pass



    def list(self, args):
        """
            list devices from inventory given
        :param args:
        """
        cmd = None

        try:
            params = self.util.get_args(args)
            #check namespace variables if set
            type = params.type
            #moderate type value to determine the statement
            if type == 'group':
                cmd = SQL.SQL_SELECT_GROUP_ALL
            elif type == 'device':
                cmd = SQL.SQL_SELECT_DEVICE_ALL
            elif type == 'config':
                cmd = SQL.SQL_SELECT_CONFIG
            elif type == 'vlan':
                cmd = SQL.SQL_SELECT_VLAN
            else:
                print Language.MSG_ERR_GENERIC.format('190', 'No [type] argument provided')

            #functions database operations
            if cmd is Empty:
                print Language.MSG_ERR_GENERIC.format("194", "SQL command could not be created")
            else:
                results = self.db.select(cmd)
                if results:
                    try:
                        for row in results:
                            print str(row).strip()
                    except Exception as e:
                        print e.message
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format("133", e.message)
            pass

    def group(self, args):
        """
            add new group with params
        """
        group = Group()
        try:
            params = self.util.get_args(args)
            #check namespace variables if set
            if params.name is Empty:
                print Language.MSG_ERR_EMPTY_NAME.format('group')
            else:
                group.setName(params.name)
            if params.config is Empty:
                print Language.MSG_ERR_EMPTY_CONFIG.format('group')
            else:
                group.setConfig(params.config)
            cmd = SQL.SQL_INSERT_GROUP.format(
                group.getName(),
                group.getConfig(),
                self.now,
                self.now
            )
            id = self.db.insert(cmd)
            if id is Empty:
                print Language.MSG_ERR_DATABASE_ERROR.format('128', 'inserting new group', id)
            else:
                print Language.MSG_ADD_NEW.format('group', id, group.getName())
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format("133", e.message)
            pass

    def configure(self, args):
        """
        """
        print ""

    def show(self, args):
        """
        """

    def vlan(self, args):
        """
        """

    def set(self, args):
        """


        :param args:
        """

    def remove(self, args):
        """
            remove device from inventory
        :param args:
        """
        id = None
        name = None
        cmd = None

        try:
            params = self.util.get_args(args)
            #check namespace variables if set
            type = params.type
            #moderate type value to determine the statement
            #check if type is group to remove the group belong to given id and name
            if type == 'group':
                if params.id is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('id'), '\n'
                    print Language.MSG_ADD_ID_HELP
                elif params.name is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('name'), '\n'
                    print Language.MSG_ADD_NAME_HELP
                else:
                    id = params.id
                    name = params.name
                    cmd = SQL.SQL_REMOVE_GROUP.format(name, id)
            #check if type is device to remove the group belong to given id and name
            elif type == 'device':
                if params.id is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('id'), '\n'
                    print Language.MSG_ADD_ID_HELP
                elif params.name is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('name'), '\n'
                    print Language.MSG_ADD_NAME_HELP
                else:
                    id = params.id
                    name = params.name
                    cmd = SQL.SQL_REMOVE_DEVICE.format(name, id)
            elif type == 'config':
                if params.name is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('name'), '\n'
                    print Language.MSG_ADD_NAME_HELP
                else:
                    id = params.id
                    cmd = SQL.SQL_INSERT_CONFIG.format(name)
            elif type == 'from':
                cmd = SQL.SQL_REMOVE_DEVICE_FROM_GROUP
            elif type == 'vlan':
                if params.id is Empty:
                    print Language.MSG_ERR_PARSER_EXCEPTION.format('id'), '\n'
                    print Language.MSG_ADD_ID_HELP
                else:
                    id = params.id
                    cmd = SQL.SQL_REMOVE_VLAN.format(id)
            else:
                print Language.MSG_ERR_GENERIC.format('186', 'No [type] argument provided')

            #functions database operations
            if cmd is Empty:
                print Language.MSG_ERR_GENERIC.format("222", "SQL command could not be created")
            else:
                self.db.remove(cmd)
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format("133", e.message)
            pass

    def help(self, args):
        """

        :param args:
        """
        formatter = parser._get_formatter()
        parser.exit(message=formatter.format_help())
        print Language.MSG_ARG_DESC
