# coding=utf-8
from src.model.Config import Config
from src.model.Request import Request

__author__ = 'fatih'


class Device(dict):
    """
        Device object class to create a runtime instance while adding a new device
    """

    def __init__(self):
        super(Device, self).__init__()
        self["ip"] = None
        self["name"] = None
        self["username"] = 'Cisco'
        self["password"] = 'Cisco'
        self["config_id"] = None
        self["config"] = Config()
        self["description"] = None

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
        self["username"] = password

    def getPassword(self):
        """
        :return:
        """
        return self["username"]

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
        :param description:
        """
        self["description"] = description

    def getDescription(self):
        """
        :return:
        """
        return self["description"]

    def setConfigID(self, config):
        """

        :param config:
        """
        self["config_id"] = config

    def getConfigID(self):
        """

        :return:
        """
        return self["config_id"]

    def setConfig(self, config):
        """

        :param config:
        """
        self["config"].update(config)

    def getConfig(self):
        """

        :return:
        """
        return self["config"]