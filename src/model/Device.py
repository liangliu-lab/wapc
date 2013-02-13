from src.model.Config import Config
from src.model.Request import Request

__author__ = 'fatih'


class Device(dict):
    """
        Device object class to create a runtime instance while adding a new device
    """
    ip = None
    name = None
    username = 'Cisco'
    password = 'Cisco'
    config_id = None
    enable_password = 'Cisco'
    personality = None
    request = Request()
    config = Config()

    def setIP(self, ip):
        self.ip = ip

    def getIP(self):
        return self.ip

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setUsername(self, username):
        self.username = username

    def getUsername(self):
        return self.username

    def setPassword(self, password):
        self.password = password

    def getPassword(self):
        return self.password

    def setConfigID(self, config):
        self.config_id = config

    def getConfigID(self):
        return self.config_id

    def setConfig(self, config):
        self.config.update(config)

    def getConfig(self):
        return self.config
