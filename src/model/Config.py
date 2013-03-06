# coding=utf-8
"""
    Config model to handle device or group configuration
"""
from src.model.Request import Request

__author__ = 'fatih'


class Config(dict):
    """
        Device configuration model to implement new instance while inserting a new device
    """

    def __init__(self):
        super(Config, self).__init__()
        self["id"] = None
        self["name"] = 'Default Device'
        self["description"] = 'Default desc for device'
        self["ip"] = "192.168.0.1"
        self["username"] = 'Username'
        self["password"] = 'Password'
        self["enable_password"] = 'Password'
        self["radius_config_id"] = 0
        self["transport_protocol"] = 'Telnet'
        self["personality"] = 'ios'
        self["ssid"] = "LBREAP"
        self["vlan_id"] = 0
        self["channel"] = 0
        self["channel_freq"] = None
        self["request"] = Request()

    def setID(self, cID):
        """
            :param cID:
            """
        self["id"] = cID

    def getID(self):
        """
            :return:
            """
        return self["id"]

    def setName(self, name):
        """

            :param name:
            """
        self["name"] = name

    def getName(self):
        """
            :return:
            """
        return self["name"]

    def setDescription(self, description):
        """
        :param self:
        :param description:
        """
        self["description"] = description

    def getDescription(self):
        """
            :return:
            """
        return self["description"]

    def setIP(self, ip):
        """

            :param ip:
            """
        self["ip"] = ip

    def getIP(self):
        """
            :return:
            """
        return self["ip"]

    def setUsername(self, username):
        """

        :param username:
        """
        self["username"] = username

    def getUsername(self):
        """
        :return:
        """
        return self["username"]

    def setPassword(self, password):
        """

        :param password:
        """
        self["password"] = password

    def getPassword(self):
        """
        :return:
        """
        return self["password"]
    
    def setEnablePassword(self, option):
        """

        :param option:
        """
        self["enable_password"] = option

    def getEnablePassword(self):
        """
        :return:
        """
        return self["enable_password"]

    def setRadiusID(self, radius_config_id):
        """

            :param radius_config_id:
            """
        self["radius_config_id"] = radius_config_id

    def getRadiusID(self):
        """

            :return:
            """
        return self["radius_config_id"]

    def setSSID(self, ssid):
        """

            :param ssid:
            """
        self["ssid"] = ssid

    def getSSID(self):
        """

            :return:
            """
        return self["ssid"]

    def setVLAN(self, vlan_id):
        """

            :param vlan_id:
            """
        self["vlan_id"] = vlan_id

    def getVLAN(self):
        """


            :return:
            """
        return self["vlan_id"]

    def setChannel(self, channel):
        """

            :param channel:
            """
        self["channel"] = channel

    def getChannel(self):
        """


            :return:
            """
        return self["channel"]

    def setChannelFreq(self, channel_freq):
        """

            :param channel_freq:
            """
        self["channel_freq"] = channel_freq

    def getChannelFreq(self):
        """


            :return:
            """
        return self["channel_freq"]

    def setTProtocol(self, protocol):
        """

            :param protocol:
            """
        self["transport_protocol"] = protocol

    def getTProtocol(self):
        """


            :return:
            """
        return self["transport_protocol"]

    def setPersonality(self, personality):
        """

            :param personality:
            """
        self["personality"] = personality

    def getPersonality(self):
        """

            :return personality:
            """
        return self["personality"]

    def setRequest(self, request):
        """
                Set request
            :param request:
            """
        self["request"].update(request)

    def getRequest(self):
        """

            :return:
            """
        return self["request"]