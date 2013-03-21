# coding=utf-8
"""
    Config model to handle device or group configuration
"""
from src.model.Request import Request

__author__ = 'fatih'


class Config(dict):
    """
        Device configuration model to implement new instance while inserting a new device
    """

    def __init__(self):
        super(Config, self).__init__()
        self["id"] = None
        self["name"] = 'Default Device'
        self["description"] = 'Default desc for device'
        self["ip"] = "192.168.0.1"
        self["username"] = 'Username'
        self["password"] = 'Password'
        self["enable_password"] = ''
        self["radius_config_id"] = 0
        self["transport_protocol"] = 'Telnet'
        self["personality"] = 'ios'
        self["ssid"] = "LBREAP"
        self["vlan_id"] = 0
        self["channel"] = 10
        self["maxclient"] = 20
        self["request"] = Request()
        self["Add Date"] = None
        self["Last Modified"] = None

    def set_id(self, cID):
        """
            :param cID:
            """
        self["id"] = cID

    def get_id(self):
        """
            :return:
            """
        return self["id"]

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
        :param self:
        :param description:
        """
        self["description"] = description

    def get_description(self):
        """
            :return:
            """
        return self["description"]

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
        self["password"] = password

    def get_password(self):
        """
        :return:
        """
        return self["password"]
    
    def set_enable_password(self, option):
        """

        :param option:
        """
        self["enable_password"] = option

    def get_enable_password(self):
        """
        :return:
        """
        return self["enable_password"]

    def set_radius(self, radius_config_id):
        """

            :param radius_config_id:
            """
        self["radius_config_id"] = radius_config_id

    def get_radius(self):
        """

            :return:
            """
        return self["radius_config_id"]

    def set_ssid(self, ssid):
        """

            :param ssid:
            """
        self["ssid"] = ssid

    def get_ssid(self):
        """

            :return:
            """
        return self["ssid"]

    def set_vlan(self, vlan_id):
        """

            :param vlan_id:
            """
        self["vlan_id"] = vlan_id

    def get_vlan(self):
        """


            :return:
            """
        return self["vlan_id"]

    def set_channel(self, channel):
        """

            :param channel:
            """
        self["channel"] = channel

    def get_channel(self):
        """


            :return:
            """
        return self["channel"]

    def set_transport_protocol(self, protocol):
        """

            :param protocol:
            """
        self["transport_protocol"] = protocol

    def get_transport_protocol(self):
        """


            :return:
            """
        return self["transport_protocol"]

    def set_personality(self, personality):
        """

            :param personality:
            """
        self["personality"] = personality

    def get_personality(self):
        """

            :return personality:
            """
        return self["personality"]

    def set_maxclient(self, request):
        """
                Set request
            :param request:
            """
        self["maxclient"].update(request)

    def get_maxclient(self):
        """

            :return:
            """
        return self["maxclient"]

    def set_request(self, request):
        """
                Set request
            :param request:
            """
        self["request"].update(request)

    def get_request(self):
        """

            :return:
            """
        return self["request"]

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