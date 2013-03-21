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
        self["username"] = "Cisco"
        self["password"] = "Cisco"
        self["brand"] = 'cisco'
        self["model"] = 'cisco'
        self["firmware"] = 'cisco'
        self["relation"] = 'slave'
        self["config_id"] = None
        self["config"] = Config()
        self["description"] = None
        self["Add Date"] = None
        self["Last Modified"] = None

    def set_id(self, dID):
        """
        :param dID:
        """
        self["id"] = dID

    def get_id(self):
        """

        :return:
        """
        return self["id"]

    def set_ip(self, ip):
        """

        :param ip:
        """
        self["ip"] = ip

    def get_ip(self):
        """

        :return:
        """
        return self["ip"]

    def set_username(self, username):
        """

        :param username:
        """
        self["username"] = username

    def get_username(self):
        """
        :return:
        """
        return self["username"]

    def set_password(self, password):
        """

        :param password:
        """
        self["username"] = password

    def get_password(self):
        """
        :return:
        """
        return self["username"]

    def set_brand(self, brand):
        """

        :param brand:
        """
        self["brand"] = brand

    def get_brand(self):
        """
        :return:
        """
        return self["brand"]

    def set_model(self, model):
        """

        :param model:
        """
        self["model"] = model

    def get_model(self):
        """
        :return:
        """
        return self["model"]

    def set_firmware(self, firmware):
        """

        :param firmware:
        """
        self["firmware"] = firmware

    def get_firmware(self):
        """
        :return:
        """
        return self["firmware"]

    def set_relation(self, relation):
        """

        :param relation:
        """
        self["relation"] = relation

    def get_relation(self):
        """
        :return:
        """
        return self["relation"]

    def set_name(self, name):
        """
        :param name:
        """
        self["name"] = name

    def get_name(self):
        """
        :return:
        """
        return self["name"]

    def set_description(self, description):
        """
        :param description:
        """
        self["description"] = description

    def get_description(self):
        """
        :return:
        """
        return self["description"]

    def set_config_id(self, config):
        """

        :param config:
        """
        self["config_id"] = config

    def get_config_id(self):
        """

        :return:
        """
        return self["config_id"]

    def set_config(self, config):
        """

        :param config:
        """
        self["config"] = config

    def get_config(self):
        """

        :return:
        """
        return self["config"]

    def set_date_add(self, date):
        """

        :param date:
        """
        self["Add Date"] = date

    def get_date_add(self):
        """

        :return:
        """
        return self["Add Date"]

    def set_date_modified(self, date):
        """

        :param date:
        """
        self["Last Modified"] = date

    def get_date_modified(self):
        """

        :return:
        """
        return self["Last Modified"]