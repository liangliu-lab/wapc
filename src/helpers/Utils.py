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
import inspect
import re
from src.resources.Resources import Resources
import src.helpers.Formatter as Formatter
from src.model.Device import Device
from src.model.Config import Config
from time import strftime, gmtime
import ConfigParser


class Utils(object):
    """
    Utils class implements utility methods to help core methods work fine,
    independent, reliable and effective.

    """
    now = None
    environment = None
    postfix = None

    def __init__(self):
        self.init_globals()

    def init_globals(self):
        """

        @return
        """
        self.now = strftime(Resources.string_time, gmtime())

        # Get system environment from system configuration file
        config_parser = ConfigParser.RawConfigParser()
        config_parser.read(Resources.__config__system__)
        self.environment = config_parser.get("system", "environment")
        self.log_db = config_parser.get("system", "log_db")
        self.master_db = config_parser.get("system", "master_db")
        Resources.cfg_section_log_db = self.log_db
        Resources.cfg_section_master_db = self.master_db

    @classmethod
    def get_clean_params(cls, args):
        """
        get_clean_params method return filtered and processed arguments gathered
        from command line into argument parser.

        Arguments retrieved with whitespaces, irregular order and mapped.
        Therefore it is need to be cleaned, reorganized and regularly mapped to
        send correct values into argument parser. This method help us to clean
        and get actual ordered parameters as a list.

        @param cls class itself
        @param args arguments list gathered from command line
        @return A fully organized and clean argument list
        """
        regex = re.compile(r"\-\S*[^\-]*", re.IGNORECASE)
        arg_list = regex.findall(args)
        return arg_list

    @classmethod
    def formatter(cls, heading, source):
        """
        Format output text as a human readable style

        @param cls is class itself
        @param heading is a list object comes from other methods to
        create a pretty table to be printed

        @param source is a tuple list aims to create pretty table rows
        """
        try:
            width = 30
            head = [str(i).replace("_", " ").upper() for i in heading]
            print Formatter.indent(
                [head] + source,
                has_header=True,
                separate_rows=True,
                prefix='| ',
                postfix=' |',
                wrapfunc=lambda x: Formatter.wrap_onspace(x, width)
            )
        except RuntimeError as exception:
            print exception.message
        except ImportError as exception:
            print exception.message

    @classmethod
    def get_line(cls):
        """
        Get current line of file to handle exception lines

        @param cls class itself

        @return Current number of line where method is called
        """
        return inspect.currentframe().f_back.f_lineno

    @classmethod
    def validate(cls, source=None, stype=None):
        """
        This method is used to validate given input source by type
        format such as IP,
        email, whitespace-free strings, etc.

        @param cls class itself

        @param type defines what sort of value will be validated.
        Recently supported keys name, eth & ip

        @param source
        """
        src = ''.join(source.split())
        regex = re.compile(Resources.REGEX[stype], re.IGNORECASE)
        arg = ''.join(regex.findall(src))
        return arg

    @classmethod
    def fix_date(cls, source):
        """
        This method aims to fix date format gathered from database.

        Database record comes from datetime.datetime formatted and this makes
        operations fails because of malformed data. So, it should be formatted
        to the regular datetime format.

        @param cls
        @param source is a dictionary
        @return formatted dictionary
        """
        try:
            if type(source) is list:
                for row in source:
                    row["Add Date"] = row["Add Date"] \
                        .strftime(Resources.time_format)
                    row["Last Modified"] = row["Last Modified"] \
                        .strftime(Resources.time_format)
            else:
                source["Add Date"] = source["Add Date"] \
                    .strftime(Resources.time_format)
                source["Last Modified"] = source["Last Modified"] \
                    .strftime(Resources.time_format)
            return source
        except ValueError as exception:
            #Logging
            pass

    @classmethod
    def wellform_dict(cls, source, keys, values):
        """
        This method aims to wellform the given source into a zipped dictionary
        from keys and values

        @param cls
        @param source dictionary source
        @param keys will be keys of new dictionary
        @param values will be values for regarding keys
        @return
        """
        wellformed_dict = dict(
            map(
                list,
                zip(source[keys], source[values])))
        return wellformed_dict

    def get_request_config(self, device=Device(), config=Config()):
        """

        @param device
        @param config
        @return target file to implement in perl script
        """
        file_name = self.now + "-" + str(device.get_id())
        target_file = Resources.input_source % {'file': file_name}

        request_config = {"ip": device.get_ip(),
                          "username": config["username"],
                          "transport_protocol": config["transport_protocol"],
                          "enable_password": config["enable_password"],
                          "password": config["password"],
                          "personality": config["personality"],
                          "request": config["request"]}

        from src.cli.CommunicationInterface import CommunicationInterface
        communication_interface = CommunicationInterface()
        communication_interface.write_source_file(request_config, target_file)

        return target_file
