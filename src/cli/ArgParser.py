# coding=utf-8
from Queue import Empty
import argparse
from src.language.language import Language

__author__ = 'fatih'


class ArgParser(object):
    """
        ArgParser object
    """

    parser = argparse.ArgumentParser(description=Language.MSG_ARG_DESC, version='2.3',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    params = ''

    def __init__(self):
        """
            Create instance

        """
        try:
            self.set_parser()
        except Exception as e:
            print e.message
            pass

    def set_parser(self):
        """
            Set parser
        """
        self.parser.add_argument('-t', '--type',
                                 dest='type',
                                 help=Language.MSG_ADD_TYPE_HELP,
                                 action='store',
                                 default='device'
        )
        self.parser.add_argument('-id', '--id',
                                 dest='id',
                                 help=Language.MSG_ADD_ID_HELP,
                                 action='store',
                                 default='0'
        )
        self.parser.add_argument('-i', '--ip',
                                 dest='ip',
                                 help=Language.MSG_ADD_IP_HELP,
                                 action='store',
                                 default='10.0.0.1'
        )
        self.parser.add_argument('-n', '--name',
                                 dest='name',
                                 help=Language.MSG_ADD_NAME_HELP,
                                 action='store',
                                 default='New Device'
        )
        self.parser.add_argument('-u', '--username',
                                 dest='username',
                                 help=Language.MSG_ADD_USERNAME_HELP,
                                 action='store',
                                 default='admin'
        )
        self.parser.add_argument('-p', '--password',
                                 dest='password',
                                 help=Language.MSG_ADD_PASSWORD_HELP,
                                 action='store',
                                 default='admin'
        )
        self.parser.add_argument('-g', '--group',
                                 dest='group',
                                 help=Language.MSG_ADD_GROUP_HELP,
                                 action='store',
                                 default='wapc'
        )
        self.parser.add_argument('-c', '--config',
                                 dest='config',
                                 help=Language.MSG_ADD_GROUP_HELP,
                                 action='store',
                                 default='wapc'
        )
        self.parser.add_argument('-s', '--subnet',
                                 dest='subnet',
                                 help=Language.MSG_ADD_SUBNET_HELP,
                                 action='store',
                                 default='255.255.255.0'
        )
        self.parser.add_argument('-d', '--device',
                                 dest='device',
                                 help=Language.MSG_ADD_DEVICE_HELP,
                                 action='store',
                                 default='12'
        )
        self.parser.add_argument('-inet', '--interface',
                                 dest='interface',
                                 help=Language.MSG_ADD_INTERFACE_HELP,
                                 action='store',
                                 default='eth0'
        )
        self.parser.add_argument('-desc', '--description',
                                 dest='description',
                                 help=Language.MSG_ADD_DESC_HELP,
                                 action='store',
                                 default='Default description for device or group included in configuration values'
        )
        self.parser.add_argument('-r', '--radius',
                                 dest='radius',
                                 help=Language.MSG_ADD_RADIUS_HELP,
                                 action='store',
                                 default='radius'
        )
        self.parser.add_argument('-sid', '--ssid',
                                 dest='ssid',
                                 help=Language.MSG_ADD_SSID_HELP,
                                 action='store',
                                 default='ssid'
        )
        self.parser.add_argument('-vid', '--vlan',
                                 dest='vlan',
                                 help=Language.MSG_ADD_VLAN_HELP,
                                 action='store',
                                 default='vlan'
        )
        self.parser.add_argument('-ch', '--channel',
                                 dest='channel',
                                 help=Language.MSG_ADD_CHANNEL_HELP,
                                 action='store',
                                 default='12',
                                 type=int
        )
        self.parser.add_argument('-fq', '--frequency',
                                 dest='frequency',
                                 help=Language.MSG_ADD_FREQ_HELP,
                                 action='store',
                                 default='5'
        )
        self.parser.add_argument('-o', '--option',
                                 dest='option',
                                 help=Language.MSG_ADD_FREQ_HELP,
                                 action='store',
                                 default=''
        )
        self.parser.add_argument('-param', '--param',
                                 dest='parameter',
                                 help=Language.MSG_ADD_FREQ_HELP,
                                 action='store',
                                 default='5'
        )

    def get_args(self, args):
        """

        :param args:
        :return:
        """
        try:
            if self.parser._get_args() is Empty:
                self.params = self.parser.parse_known_args(args)
            else:
                self.params = self.parser.parse_args(args.split())
        except Exception as e:
            print Language.MSG_ERR_ARG_PARSE_GET.format(e.message)
            pass
        return self.params

