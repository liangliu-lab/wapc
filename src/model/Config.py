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
        self.id = id
    def getID(self):
        return self.id

    def setName(self,name):
        self.name = name
    def getName(self):
        return self.name

    def setDescription(self,description):
        self.description = description
    def getDescription(self):
        return self.description

    def setIP(self,ip):
        self.ip = ip
    def getIP(self):
        return self.ip

    def setRadiusID(self,radius_config_id):
        self.radius_config_id = radius_config_id
    def getRadiusID(self):
        return self.radius_config_id

    def setSSID(self,ssid):
        self.ssid = ssid
    def getSSID(self):
        return self.ssid

    def setGroup(self, group):
        self.group = group
    def getGroup(self):
        return self.group

    def setVLAN(self,vlan_id):
        self.vlan_id = vlan_id
    def getVLAN(self):
        return self.vlan_id

    def setChannel(self, channel):
        self.channel = channel
    def getChannel(self):
        return self.channel

    def setChannelFreq(self,channel_freq):
        self.channel_freq = channel_freq
    def getChannelFreq(self):
        return self.channel_freq

    def setTProtocol(self, protocol):
        self.transport_protocol = protocol
    def getTProtocol(self):
        return self.transport_protocol

    def setPersonality(self, personality):
        self.personality = personality
    def getPersonality(self):
        return self.personality


