# coding=utf-8
"""
    Implements VLan methods to configure, create, assign, remove vlan(s)
"""

import threading
from time import strftime, gmtime
from src.cli.CommunicationInterface import CommunicationInterface
from src.helpers.Utils import Utils
from src.database.Database import Database
from src.model.Device import Device
from src.resources.Resources import Resources

__author__ = 'fatih'


class VLanMethods(threading.Thread):
    """
    Implements VLan methods to configure, create, assign, remove vlan(s)
    """

    def __init__(self):
        """
            """
        super(VLanMethods, self).__init__()
        self.utils = Utils()
        self.db = Database()
        self.ci = CommunicationInterface()
        self.script = Resources.ci_script
        self.cfg_device = Resources.cfg_device_resource
        self.now = strftime(Resources.time_format, gmtime())
        self.device = Device()

    def create(self, params):
        """
            Add function to implement a thread at background responds to
            Web or CLI request
        :param params:
        """
        pass

    def read(self, vid):
        """

        :param vid:
        """

    def update(self, params):
        """
        :param params:
        """

    def delete(self, params):
        """


        :param params:
        """

    def set(self, params):
        """
            This methods handle options and connect throug device by given name
        :param params:
        """

    def group(self, params):
        """
            This methods groups given device id. Before this method to be
            implemented user should execute ls command
            to see what device(s) recorded in database.
            :param params:
        """

    def show(self, params):
        """

        :param params:
        """