# coding=utf-8
"""
    Device model
"""
from src.model.Config import Config

__author__ = 'fatih'


class Device(dict):
    """
        Device object class to create a runtime instance while adding a new device
    """

    def __init__(self):
        super(Device, self).__init__()
        self["id"] = None
        self["ip"] = None
        self["name"] = None
        self["brand"] = 'cisco'
        self["model"] = 'cisco'
        self["firmware"] = 'cisco'
        self["relation"] = 'slave'
        self["config_id"] = None
        self["config"] = Config()
        self["description"] = None

    def setID(self, dID):
        """
        :param dID:
        """
        self["id"] = dID

    def getID(self):
        """

        :return:
        """
        return self["id"]

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

    def setBrand(self, brand):
        """

        :param brand:
        """
        self["brand"] = brand

    def getBrand(self):
        """
        :return:
        """
        return self["brand"]

    def setModel(self, model):
        """

        :param model:
        """
        self["model"] = model

    def getModel(self):
        """
        :return:
        """
        return self["model"]

    def setFirmware(self, firmware):
        """

        :param firmware:
        """
        self["firmware"] = firmware

    def getFirmware(self):
        """
        :return:
        """
        return self["firmware"]

    def setRelation(self, relation):
        """

        :param relation:
        """
        self["relation"] = relation

    def getRelation(self):
        """
        :return:
        """
        return self["relation"]

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
        self["config"] = config

    def getConfig(self):
        """

        :return:
        """
        return self["config"]