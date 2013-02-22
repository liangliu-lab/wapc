# coding=utf-8
from Queue import Empty
import json
from src.config.__sql__ import SQL
from src.language.language import Language
from src.model.Commands import Commands
from src.model.Config import Config
from src.model.Device import Device
from src.model.Request import Request
from src.model.Response import Response
from src.resources.resources import Resources

__author__ = 'fatih'


class VLanMethods(object):
    """
        VLan Methods
    """
    def create(self, params):
        """
            Add function to implement a thread at background responds to Web or CLI request
        :param params:
        :param args:
        """
        device = Device()
        config = Config()
        resp = Response()
        request = Request()
        commands = Commands()

        try:
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
            print e.message
            pass

    def read(self, params):
        """

        """

    def update(self, params):
        """

        """

    def delete(self, params):
        """

        """
