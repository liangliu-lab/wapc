# coding=utf-8
from src.model.Commands import Commands

__author__ = 'fatih'


class Request(dict):
    """
        Request object class to generate a new request
        "enable":true,
        "configure":false,
        "commands":[
            {
                "command":"showa dot11 bssid"
            }
        ]
    """
    def __init__(self):
        super(Request, self).__init__()
        self["enable"] = True
        self["configure"] = False
        self["commands"] = Commands()

    def setEnable(self, status):
        """

        :param status:
        """
        self["enable"] = status

    def getEnable(self):
        """

        :return:
        """
        return self["enable"]

    def setConfigure(self, status):
        """

        :param status:
        """
        self["configure"] = status

    def getConfigure(self):
        """


        :return:
        """
        return self["configure"]

    def setCommands(self, commands):
        """

        :param commands:
        """
        self["commands"] = commands

    def getCommands(self):
        """


        :return:
        """
        return self["commands"]

    def addCommand(self, command):
        self["commands"].append(command)