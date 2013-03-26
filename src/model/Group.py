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
from src.model.Device import Device


class Group(Device):
    """
    Group class to create a runtime instance while adding a new device

    @implements Device
    """

    def __init__(self):
        super(Group, self).__init__()
        self["id"] = None
        self["name"] = None
        self["config_id"] = 0
        self["description"] = None
        self["added"] = None
        self["modified"] = None