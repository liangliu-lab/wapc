# coding=utf-8
__author__ = 'fatih'


class VLan(object):
    """
        VLan object
    """
    name = None
    ip = None
    subnet = None
    number = None
    interface = None

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setIP(self, ip):
        self.ip = ip

    def getIP(self):
        return self.ip

    def setSubnet(self, subnet):
        self.subnet = subnet

    def getSubnet(self):
        return self.subnet

    def setNumber(self, number):
        self.number = number

    def getNumber(self):
        return self.number

    def setInterface(self, interface):
        self.interface = interface

    def getInterface(self):
        return self.interface