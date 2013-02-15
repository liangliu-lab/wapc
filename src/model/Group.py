# coding=utf-8
__author__ = 'fatih'


class Group(object):
    """
        Group class to create a runtime instance while adding a new device
    """
    name = None
    config_id = None

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

    def setConfig(self, config):
        """

        :param config:
        """
        self.config_id = config

    def getConfig(self):
        """

        :return:
        """
        return self.config_id