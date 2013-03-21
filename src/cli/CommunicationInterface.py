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

CommunicationInterface class aims to handle files to provide
a processed output for inherited metdhos running in application

@package cli
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

"""
import json
import os
import subprocess
from src.language.language import Language
from src.resources.resources import Resources
from src.helper.Utils import Utils

__author__ = 'fatih'


class CommunicationInterface(object):
    """
        Communication interface class to talk with perl script
    """
    def __init__(self):
        self.utils = Utils()

    def get_source_config(self, source_file):
        """
            Get input json file to parse with params
        :param source_file:
        """
        try:
            new_config = open(source_file, 'r')
            config_source = new_config.read()
            new_config.close()
            return config_source
        except IOError as exception:
            print Language.MSG_ERR_COMM_INTERFACE_FAILED % \
                {'line': self.utils.get_line(), 'exception': exception.message}
        except BufferError as exception:
            print Language.MSG_ERR_COMM_INTERFACE_FAILED % \
                {'line': self.utils.get_line(), 'exception': exception.message}

    def call_communication_interface(self, source):
        """
            Call script with source json data file path
        :param source: 
            Usage: call_communication_interface('config.json')
        """
        try:
            response = subprocess.Popen(
                [Resources.ci_script, source],
                stdout=subprocess.PIPE
            ).communicate()[0]
            return response
        except IOError as exception:
            print Language.MSG_ERR_COMM_INTERFACE_FAILED % \
                {'line': self.utils.get_line(), 'exception': exception.message}
        except BufferError as exception:
            print Language.MSG_ERR_COMM_INTERFACE_FAILED % \
                {'line': self.utils.get_line(), 'exception': exception.message}

    def write_source_file(self, source, target, p_type='JSON'):
        """
            Write source file to provide the communication interface
        :param p_type:
        :param target:
        :param source:
        """
        try:
            new_config = open(target, 'w+')
            if p_type is 'JSON':
                new_config.write(json.dumps(source))
            elif p_type is 'RAW':
                new_config.write(source)
            elif p_type is 'XML':
                # Convert source into XML file will be implemented
                pass
            else:
                new_config.write(source)
            new_config.close()
        except IOError as exception:
            print Language.MSG_ERR_COMM_INTERFACE_FAILED % \
                {'line': self.utils.get_line(), 'exception': exception.message}
        except BufferError as exception:
            print Language.MSG_ERR_COMM_INTERFACE_FAILED % \
                {'line': self.utils.get_line(), 'exception': exception.message}

    def backup(self, source, target, time, p_type='RAW'):
        """


        :param p_type:
        :rtype : object
        :param source: 
        :param target: 
        :param time: 
        """
        try:
            backup_folder = Resources.BACKUP_PATH + target
            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)
            new_backup = open(
                backup_folder + "/" +
                Resources.back_name.format(time.replace(' ', '-')), 'w+')
            if p_type is 'JSON':
                new_backup.write(json.dumps(source))
            elif p_type is 'RAW':
                new_backup.write(source)
            elif p_type is 'XML':
                # Convert source into XML file will be implemented
                pass
            new_backup.close()
        except IOError as exception:
            print Language.MSG_ERR_COMM_INTERFACE_FAILED % \
                {'line': self.utils.get_line(), 'exception': exception.message}
        except BufferError as exception:
            print Language.MSG_ERR_COMM_INTERFACE_FAILED % \
                {'line': self.utils.get_line(), 'exception': exception.message}

