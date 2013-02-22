# coding=utf-8
__author__ = 'fatih'


class Group(object):
    """
        Group class to create a runtime instance while adding a new device
    """
    def __init__(self):
        self.name = None
        self.config_id = None
        self.description = None
        self.added = None
        self.modified = None

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

    def setAdded(self, date):
        """

        :param date:
        """
        self.added = date

    def getAdded(self):
        """

        :return:
        """
        return self.added

    def setModified(self, date):
        """

        :param date:
        """
        self.modified = date

    def getModified(self):
        """

        :return:
        """
        return self.modified