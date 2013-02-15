from src.model.Config import Config
from src.model.Request import Request

__author__ = 'fatih'


class NewDevice(dict):
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
        """

        :param ip:
        """
        self.ip = ip

    def getIP(self):
        """

        :return:
        """
        return self.ip

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

    def setUsername(self, username):
        """
        :param username:
        """
        self.username = username

    def getUsername(self):
        """


        :return:
        """
        return self.username

    def setPassword(self, password):
        """

        :param password:
        """
        self.password = password

    def getPassword(self):
        """

        :return:
        """
        return self.password

    def setConfigID(self, config):
        """

        :param config:
        """
        self.config_id = config

    def getConfigID(self):
        """

        :return:
        """
        return self.config_id

    def setConfig(self, config):
        """

        :param config:
        """
        self.config.update(config)

    def getConfig(self):
        """

        :return:
        """
        return self.config