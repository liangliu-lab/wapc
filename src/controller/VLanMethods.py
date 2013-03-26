# coding=utf-8
"""
    Implements VLan methods to configure, create, assign, remove vlan(s)
"""

import threading
from time import strftime, gmtime
from src.cli.CommunicationInterface import CommunicationInterface
from src.resources.SQL import SQL
from src.helper.Utils import Utils
from src.database.Database import Database
from src.language.Language import Language
from src.model.Device import Device
from src.resources.Resources import Resources

__author__ = 'fatih'


class VLanMethods(threading.Thread):
    """
        VLan methods
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
            Add function to implement a thread at background responds to Web or CLI request
        :param params:
        """
        pass

    def read(self, vid):
        """

        :param vid:
        """
        try:
            #check namespace variables if set

            #moderate type value to determine the statement
            cmd = SQL.SQL_SELECT_VLAN_DETAIL % {'id': int(vid)}
            fields, results = self.db.select(cmd)
            if fields and results:
                try:
                    rset = {"fields": fields, "results": [list(f) for f in results][0]}
                    return rset
                except Exception as e:
                    print e.message
                    pass
            else:
                raise Exception(
                    Language.MSG_ERR_GENERIC.format(self.utils.get_line(), "There is no device record found on table"))
        except Exception as e:
            print Language.MSG_ERR_GENERIC.format(self.utils.get_line(), e.message)
            pass

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
            This methods groups given device id. Before this method to be implemented user should execute ls command
            to see what device(s) recorded in database.
            :param params:
        """

    def show(self, params):
        """

        :param params:
        """