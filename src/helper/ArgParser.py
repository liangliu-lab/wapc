# coding=utf-8
"""
    ArgParser class
"""
from Queue import Empty
import argparse
from src.language.language import Language

__author__ = 'fatih'


class ArgParser(object):
    """
        ArgParser object
    """

    parser = argparse.ArgumentParser(description=Language.MSG_ARG_DESC, version='2.3',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
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
            This methos parsing retrieved arguments into namespace variables

        """
        self.parser.add_argument('-b', '--brand',
                                 dest='brand',
                                 help=Language.MSG_ADD_BRAND_HELP,
                                 action='store'
        )
        self.parser.add_argument('-d', '--device',
                                 dest='device',
                                 help=Language.MSG_ADD_DEVICE_HELP,
                                 action='store'
        )
        self.parser.add_argument('-D', '--desc',
                                 dest='description',
                                 help=Language.MSG_ADD_DESC_HELP
        )
        self.parser.add_argument('-e', '--inet',
                                 dest='interface',
                                 help=Language.MSG_ADD_INTERFACE_HELP,
                                 action='store'
        )
        self.parser.add_argument('-f', '--frequency',
                                 dest='frequency',
                                 help=Language.MSG_ADD_FREQ_HELP,
                                 action='store'
        )
        self.parser.add_argument('-F', '--firmware',
                                 dest='firmware',
                                 help=Language.MSG_ADD_FIRMWARE_HELP,
                                 action='store'
                                 )
        self.parser.add_argument('-g', '--group',
                                 dest='group',
                                 help=Language.MSG_ADD_GROUP_HELP,
                                 action='store'
        )
        self.parser.add_argument('-H', '--channel',
                                 dest='channel',
                                 help=Language.MSG_ADD_CHANNEL_HELP,
                                 action='store',
                                 type=int
        )
        self.parser.add_argument('-i', '--id',
                                 dest='id',
                                 help=Language.MSG_ADD_ID_HELP,
                                 action='store'
        )
        self.parser.add_argument('-I', '--ip',
                                 dest='ip',
                                 help=Language.MSG_ADD_IP_HELP,
                                 action='store'
        )
        self.parser.add_argument('-m', '--model',
                                 dest='model',
                                 help=Language.MSG_ADD_MODEL_HELP,
                                 action='store'
        )
        self.parser.add_argument('-n', '--name',
                                 dest='name',
                                 help=Language.MSG_ADD_NAME_HELP,
                                 action='store'
        )
        self.parser.add_argument('-o', '--option',
                                 dest='option',
                                 help=Language.MSG_ADD_FREQ_HELP,
                                 action='store'
        )
        self.parser.add_argument('-p', '--password',
                                 dest='password',
                                 help=Language.MSG_ADD_PASSWORD_HELP,
                                 action='store'
        )
        self.parser.add_argument('-P', '--param',
                                 dest='parameter',
                                 help=Language.MSG_ADD_FREQ_HELP,
                                 action='store'
        )
        self.parser.add_argument('-r', '--radius',
                                 dest='radius',
                                 help=Language.MSG_ADD_RADIUS_HELP,
                                 action='store'
        )
        self.parser.add_argument('-R', '--relation',
                                 dest='relation',
                                 help=Language.MSG_ADD_RELATION_HELP,
                                 action='store'
        )
        self.parser.add_argument('-s', '--subnet',
                                 dest='subnet',
                                 help=Language.MSG_ADD_SUBNET_HELP,
                                 action='store'
        )
        self.parser.add_argument('-S', '--ssid',
                                 dest='ssid',
                                 help=Language.MSG_ADD_SSID_HELP,
                                 action='store'
        )
        self.parser.add_argument('-t', '--type',
                                 dest='type',
                                 help=Language.MSG_ADD_TYPE_HELP,
                                 action='store'
        )
        self.parser.add_argument('-u', '--username',
                                 dest='username',
                                 help=Language.MSG_ADD_USERNAME_HELP,
                                 action='store'
        )
        self.parser.add_argument('-V', '--vlan',
                                 dest='vlan',
                                 help=Language.MSG_ADD_VLAN_HELP,
                                 action='store'
        )

    def get_args(self, args):
        """

        :param args:
        :return:
        """
        try:
            if self.parser._get_args() is Empty:
                self.params = self.parser.parse_known_args(args.split())
            else:
                self.params = self.parser.parse_args(args)
        except Exception as e:
            raise Exception(Language.MSG_ERR_ARG_PARSE_GET.format(e.message))
            pass
        return self.params

