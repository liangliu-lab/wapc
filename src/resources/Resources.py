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

@package resources
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

"""


class Resources(object):
    """
    Resources file covers all required global variables,
    path names, file names, etc.

    You need to configure only this file anytime you need to change variables
    """
    #path variables
    ROOT_PATH = "/opt/labris/sbin/wapc/"
    SOURCE_PATH = ROOT_PATH + "src/"
    INCLUDE_PATH = SOURCE_PATH + "include/"
    CONFIG_PATH = SOURCE_PATH + "config/"
    BACKUP_PATH = SOURCE_PATH + "backup/"

    #communication interface script
    ci_script = INCLUDE_PATH + "labris-wap-controller.pl"

    #communication interface script source file
    ci_source = INCLUDE_PATH + "input.json"
    input_source = INCLUDE_PATH + "%(file)s.json"

    #defulat config commands for brand new addded device
    ci_config = INCLUDE_PATH + "default.json"

    # initial config will ve set to
    device_initial_config = CONFIG_PATH + '%(path)s/%(relation)s-config.conf'
    device_load_command = INCLUDE_PATH + "load.json"
    device_tftp_file = '%(relation)s-config.conf'
    device_tftp_path = "/var/tftpboot/" + device_tftp_file

    #global device config file resource
    cfg_device_resource = CONFIG_PATH + "wapc_config.json"

    #database config file
    __db__config__ = CONFIG_PATH + "database.cfg"

    # system environment configuration
    __config__system__ = CONFIG_PATH + "config.cfg"

    #backup file name
    back_name = "backup-{0}.bak"

    #shell initial prompt
    prompt = "WAPC:~ cli$ "

    #global recent time format
    time_format = "%Y-%m-%d %H:%M:%S"
    string_time = "%Y%m%d_%H%M%S"

    #config file variables for system databases
    cfg_section_master_db = "master_db"
    cfg_section_log_db = "log_db"
    cfg_section_system = "system"

    #config file variables for mysql
    cfg_section_mysql = "mysql"

    #======== Regex patterns =========
    #
    #=================================
    REGEX = dict(name='^[a-zA-Z0-9]+$',
                 ip='^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.)'
                    '{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
                 eth='^(\\w){1,6}[0-9]{1,3}([:.][0-9]{1,3})?$')

