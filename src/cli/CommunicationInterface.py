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
a processed output for inherited methods running in application

@package cli
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

"""
import json
import os
import subprocess
from src.language.Language import Language
from src.resources.Resources import Resources
from src.helpers.Utils import Utils

__author__ = 'fatih'


class CommunicationInterface(object):
    """
    Command list to implement all required methods pre-defined

    ConsoleInterface has been inherited from cmd library to handle
    commandline interface with user interaction. This class gathers commands
    from user and declare them into individual methods written in project
    own classes.

    """
    def __init__(self):
        """
        Constructure of ConsoleInterface class

        """
        self.utils = Utils()

    def get_source_config(self, source_file):
        """
        get_source_config method read a file content and return as it is
        with no proceed

        @throw IOError exception
        @throw BufferError exception

        @param source_file source file will be read
        @return config_source file content expected as a configuration
        """
        try:
            new_config = open(source_file, 'r')
            config_source = new_config.read()
            new_config.close()
            return config_source
        except IOError as exception:
            raise BaseException(
                Language.MSG_ERR_COMM_INTERFACE_FAILED %
                {
                    'line': self.utils.get_line(),
                    'exception': exception.message
                }
            )
        except BaseException as exception:
            raise BaseException(
                Language.MSG_ERR_COMM_INTERFACE_FAILED %
                {
                    'line': self.utils.get_line(),
                    'exception': exception.message
                }
            )

    def call_communication_interface(self, source):
        """
        call_communication_interface method call perl script to communicate with
        devices. The Perl script located under "include" folder

        @throw IOError exception
        @throw BufferError exception
        @param source source is a input file includes a JSON content as commands
        and connection parameters.

        @return response as a output of subprocessed execution as JSON
        possible return responses may be one of below:
        @return NO_ERROR => 110;
        @return NET_APPLIANCE_ERROR => 100;
        @return NET_APPLIANCE_EXCEPTION => 101;
        @return FILE_OPEN_ERROR => 102;
        @return FILE_CLOSE_ERROR => 103;
        @return UNKNOWN_ERROR => 104;
        """
        try:
            response = subprocess.Popen(
                [Resources.ci_script, source],
                stdout=subprocess.PIPE
            ).communicate()[0]
            return response
        except IOError as exception:
            raise BaseException(
                Language.MSG_ERR_COMM_INTERFACE_FAILED %
                {
                    'line': self.utils.get_line(),
                    'exception': exception.message
                }
            )
        except BaseException as exception:
            raise BaseException(
                Language.MSG_ERR_COMM_INTERFACE_FAILED %
                {
                    'line': self.utils.get_line(),
                    'exception': exception.message
                }
            )

    def write_source_file(self, source, target, p_type='JSON'):
        """
        write_source_file method write the given source into targeted file
        according to the given type.

        @throw IOError exception
        @throw BufferError exception
        @param source Source is a tuple object includes object details such as
        device or config to be written in a file as a JSON.

        @param target Is the targeted file the source will be written inside.

        @param p_type Defines the kind of proceed to write the content into file
        such as raw buffer, json or xml
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
            raise BaseException(
                Language.MSG_ERR_COMM_INTERFACE_FAILED %
                {
                    'line': self.utils.get_line(),
                    'exception': exception.message
                }
            )
        except BufferError as exception:
            raise BaseException(
                Language.MSG_ERR_COMM_INTERFACE_FAILED %
                {
                    'line': self.utils.get_line(),
                    'exception': exception.message
                }
            )

    def backup(self, source, target, time, p_type='RAW'):
        """
        backup method create a backup inside a folder created with device name
        and includes a .bak file to keep the source will be backed up.

        @throw IOError exception
        @throw BufferError exception
        @param source Source is a tuple object includes object details such as
        device or config to be written in a file as a JSON.

        @param target Is the targeted file the source will be written inside.

        @param time Is the timestamp to sign the target file.

        @param p_type Defines the kind of proceed to write the content into file
        such as raw buffer, json or xml
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
            raise BaseException(
                Language.MSG_ERR_COMM_INTERFACE_FAILED %
                {
                    'line': self.utils.get_line(),
                    'exception': exception.message
                }
            )
        except BufferError as exception:
            raise BaseException(
                Language.MSG_ERR_COMM_INTERFACE_FAILED %
                {
                    'line': self.utils.get_line(),
                    'exception': exception.message
                }
            )

