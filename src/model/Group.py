# coding=utf-8
"""
    Group model for create group instance determine database column field
"""
__author__ = 'fatih'


class Group(object):
    """
        Group class to create a runtime instance while adding a new device
    """
    def __init__(self):
        self.id = None
        self.name = None
        self.config_id = 0
        self.description = None
        self.added = None
        self.modified = None

    def set_id(self, gID):
        """
            Regular setter for Group model id
        :param gID:
        """
        self.id = gID

    def get_id(self):
        """
            Regular getter for Group model
        :return id:
        """
        return self.id

    def set_name(self, name):
        """

        :param name:
        """
        self.name = name

    def get_name(self):
        """

        :return:
        """
        return self.name

    def set_config(self, config):
        """

        :param config:
        """
        self.config_id = config

    def get_config(self):
        """

        :return:
        """
        return self.config_id

    def set_description(self, description):
        """

        :param description:
        """
        self.description = description

    def get_description(self):
        """

        :return:
        """
        return self.description

    def set_date_add(self, date):
        """

        :param date:
        """
        self.added = date

    def get_date_add(self):
        """

        :return:
        """
        return self.added

    def set_date_modified(self, date):
        """

        :param date:
        """
        self.modified = date

    def get_date_modified(self):
        """

        :return:
        """
        return self.modified