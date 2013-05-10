# coding=utf-8
"""
Copyright 2013 Labris Technology.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@package helper
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

"""
import argparse
from src.language.Language import Language
from Queue import Empty
from gettext import gettext as _


class ArgParser(argparse.ArgumentParser):
    """
    AgrParser is a class aims to parse arguments gathered from command line
    actually ConsoleInterface class.

    This class parses arguments and generate a namespace with arguments came
    from Main controller and procssed by Utils.get_clean_params.
    """

    def __init__(self):
        """
            Constructor of ArgParser
        """
        super(ArgParser, self).__init__()
        language = Language()
        self.description = language.MSG_ARG_DESC
        self.version = 'v1.0.0'
        self.formatter_class = argparse.RawDescriptionHelpFormatter
        self.add_help = False

        self.params = ''
        try:
            self.set_parser()
        except BaseException as exception:
            print exception.message

    def set_parser(self):
        """
        set_parser method pre-defines arguments what will be parsed after
        instance created.

        set_parser initiates namespace attributes listed below:

        <ul>
        <li><strong>-i,--id</strong> Provide ID address to determine the
        variable with usage id</li>
        <li><strong>-I,--ip</strong> Provide IP address for the newly added
        device with usage to connect</li>
        <li><strong>-n,--name</strong> Provide name for the newly added device
        with usage name</li>
        <li><strong>-u,--username</strong> Provide username for the newly added
        device with usage username</li>
        <li><strong>-p,--password</strong> Provide password for given username
        of the newly added device with usage password</li>
        <li><strong>-P,--param</strong> Provide a parameter to be set to the
        given option</li>
        <li><strong>-g,--group</strong> Add device to the group with usage
        group</li>
        <li><strong>-c,--config</strong> Add new configuration and map it to
        the given group or device</li>
        <li><strong>-s,--subnet</strong> Define subnet for VLAN will be
        configured with usage 255.255.255.0</li>
        <li><strong>-d,--device</strong> Provide device id to add provided
        device to the group</li>
        <li><strong>-D,--description</strong> Provide a short description for
        group or device with usage</li>
        <li><strong>-r,--radius</strong> Provide Radius id to configure radius
        authentication for group or device with usage radius_id</li>
        <li><strong>-S,--ssid</strong> Provide SSID for group or device with
        usage ssid</li>
        <li><strong>-V,--vlan</strong> Provide VLAN id to determine VLAN for
        group or device with usage vlan_id</li>
        <li><strong>-H,--channel</strong> Provide channel to configure for
        group or device with usage channel</li>
        <li><strong>-t,--type</strong> Provide type of group/device/config/vlan
        from database with usage group/device/config/vlan others will cause
        error(s)</li>
        <li><strong>-o,--option</strong> Provide type of
        group/device/config/vlan from database with usage
        group/device/config/vlan</li>
        </ul>
        """

        self.add_argument('-b', '--brand',
                          dest='brand',
                          help=Language.MSG_ADD_BRAND_HELP,
                          action='store'
        )
        self.add_argument('-c', '--config',
                          dest='config',
                          help=Language.MSG_ADD_CONFIG,
                          action='store'
        )
        self.add_argument('-D', '--desc',
                          dest='description',
                          help=Language.MSG_ADD_DESC_HELP
        )
        self.add_argument('-e', '--inet',
                          dest='interface',
                          help=Language.MSG_ADD_INTERFACE_HELP,
                          action='store'
        )
        self.add_argument('-F', '--firmware',
                          dest='firmware',
                          help=Language.MSG_ADD_FIRMWARE_HELP,
                          action='store'
        )
        self.add_argument('-g', '--group',
                          dest='group',
                          help=Language.MSG_ADD_GROUP_HELP,
                          action='store'
        )
        self.add_argument('-i', '--id',
                          dest='id',
                          help=Language.MSG_ADD_ID_HELP,
                          action='store'
        )
        self.add_argument('-I', '--ip',
                          dest='ip',
                          help=Language.MSG_ADD_IP_HELP,
                          action='store'
        )
        self.add_argument('-m', '--model',
                          dest='model',
                          help=Language.MSG_ADD_MODEL_HELP,
                          action='store'
        )
        self.add_argument('-n', '--name',
                          dest='name',
                          help=Language.MSG_ADD_NAME_HELP,
                          action='store'
        )
        self.add_argument('-o', '--option',
                          dest='option',
                          help=Language.MSG_ADD_OPTION_HELP,
                          action='store'
        )
        self.add_argument('-p', '--password',
                          dest='password',
                          help=Language.MSG_ADD_PASSWORD_HELP,
                          action='store'
        )
        self.add_argument('-P', '--param',
                          dest='param',
                          help=Language.MSG_ADD_PARAM_HELP,
                          action='store'
        )
        self.add_argument('-R', '--relation',
                          dest='relation',
                          help=Language.MSG_ADD_RELATION_HELP,
                          action='store'
        )
        self.add_argument('-s', '--subnet',
                          dest='subnet',
                          help=Language.MSG_ADD_SUBNET_HELP,
                          action='store'
        )
        self.add_argument('-t', '--type',
                          dest='type',
                          help=Language.MSG_ADD_TYPE_HELP,
                          action='store'
        )
        self.add_argument('-u', '--username',
                          dest='username',
                          help=Language.MSG_ADD_USERNAME_HELP,
                          action='store'
        )
        self.add_argument('-V', '--vlan',
                          dest='vlan',
                          help=Language.MSG_ADD_VLAN_HELP,
                          action='store'
        )

    def get_args(self, args):
        """
        get_args check existing argument namespace and return this namespace.

        get_args method checks is recent ArgParser instance has already created
        arguments namespace and return known arguments. It there is no arguments
        namespace has been set it calls parse_args then return parsed arguments.

        @param args is gathered from commandline interface via cmd library

        @return parsed arguments as a namespace list
        """
        try:
            if self._get_args() is Empty:
                self.params = self.parse_known_args(args.split())
            else:
                self.params = self.parse_args(args)
            return self.params
        except BaseException as exception:
            raise BaseException(
                Language.MSG_ERR_ARG_PARSE_GET.format(exception.message)
            )

    def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        if argv:
            msg = _('unrecognized arguments: %s')
            self.error(msg % ' '.join(argv))
        return args

    def error(self, message):
        """error(message: string)

        Prints a usage message incorporating the message to stderr and
        exits.

        If you override this in a subclass, it should not return -- it
        should either exit or raise an exception.
        """
        # self.print_usage(_sys.stderr)
        # self.exit(2, _('%s: error: %s\n') % (self.prog, message))
        raise BaseException('%s: error: %s\n') % (self.prog, message)


