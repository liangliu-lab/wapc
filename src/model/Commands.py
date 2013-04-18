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

@package model
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

"""


class Commands(list):
    """
        Commands object defines a Commands

        Commands object defines a Commands model to gather command related with
        given arguments from a pre-defined commands list in a JSON file and map
        them into Commands model.
    """

    def __init__(self):
        """
        Constructor of Commands model
        """
        super(Commands, self).__init__()
        self.command = None
        self.param = None

    def set_command(self, command):
        """
        Setter to set a command belong this model

        @param command
        """
        self.command = command

    def get_command(self):
        """
        Getter for Commands model

        @return command
        """
        return self.command

    def set_param(self, param):
        """
        Setter for related param belong to any command

        @param param
        """
        self.param = param

    def get_param(self):
        """
        Getter for param

        @return related param
        """
        return self.param