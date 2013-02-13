from src.model.Commands import Commands

__author__ = 'fatih'


class Config(dict):
    """
        Device configuration model to implement new instance while inserting a new device
    """
    id = None
    name = None
    description = None
    ip = None
    radius_config_id = 0
    transport_protocol = 'Telnet'
    personality = 'ios'
    ssid = 0
    group = 0
    vlan_id = 0
    channel = 0
    channel_freq = None
    commands = Commands()

    def __init__(self):
        self.name = 'Default Device'
        self.description = 'Default desc for device'
        self.ip = "192.168.0.1"

    def setID(self, id):
        """

        :param id:
        """
        self.id = id

    def getID(self):
        """


        :return:
        """
        return self.id

    def setName(self, name):
        """

        :param name:
        """
        self.name = name

    def getName(self):
        """


        :return:
        """
        return self.name

    def setDescription(self, description):
        """

        :param description:
        """
        self.description = description

    def getDescription(self):
        """


        :return:
        """
        return self.description

    def setIP(self, ip):
        """

        :param ip:
        """
        self.ip = ip

    def getIP(self):
        """


        :return:
        """
        return self.ip

    def setRadiusID(self, radius_config_id):
        """

        :param radius_config_id:
        """
        self.radius_config_id = radius_config_id

    def getRadiusID(self):
        """


        :return:
        """
        return self.radius_config_id

    def setSSID(self, ssid):
        """

        :param ssid:
        """
        self.ssid = ssid

    def getSSID(self):
        """


        :return:
        """
        return self.ssid

    def setGroup(self, group):
        """

        :param group:
        """
        self.group = group

    def getGroup(self):
        """


        :return:
        """
        return self.group

    def setVLAN(self, vlan_id):
        """

        :param vlan_id:
        """
        self.vlan_id = vlan_id

    def getVLAN(self):
        """


        :return:
        """
        return self.vlan_id

    def setChannel(self, channel):
        """

        :param channel:
        """
        self.channel = channel

    def getChannel(self):
        """


        :return:
        """
        return self.channel

    def setChannelFreq(self, channel_freq):
        """

        :param channel_freq:
        """
        self.channel_freq = channel_freq

    def getChannelFreq(self):
        """


        :return:
        """
        return self.channel_freq

    def setTProtocol(self, protocol):
        """

        :param protocol:
        """
        self.transport_protocol = protocol

    def getTProtocol(self):
        """


        :return:
        """
        return self.transport_protocol

    def setPersonality(self, personality):
        """

        :param personality:
        """
        self.personality = personality

    def getPersonality(self):
        """


        :return:
        """
        return self.personality