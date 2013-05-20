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

@package language
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

"""


class Language(object):
    """
    Language class aims to provide required statement to requester class
    or methods to read matching locale string with given language code.
    """

    def __init__(self):
        """
        Constructor of Language class
        """
        self.MSG_ARG_DESC = self.MSG_ARG_DESC.format(
            Language.MSG_CMD_ADD_HELP,
            Language.MSG_CMD_EDIT_HELP,
            Language.MSG_CMD_GROUP_HELP,
            Language.MSG_CMD_SET_HELP,
            Language.MSG_CMD_UNSET_HELP,
            Language.MSG_CMD_LIST_HELP,
            Language.MSG_CMD_SHOW_HELP,
            Language.MSG_CMD_REMOVE_HELP,
            Language.MSG_CMD_SELFTEST_HELP,
            Language.MSG_ADD_ID_HELP,
            Language.MSG_ADD_IP_HELP,
            Language.MSG_ADD_NAME_HELP,
            Language.MSG_ADD_USERNAME_HELP,
            Language.MSG_ADD_PASSWORD_HELP,
            Language.MSG_ADD_PARAM_HELP,
            Language.MSG_ADD_GROUP_HELP,
            Language.MSG_ADD_CONFIG,
            Language.MSG_ADD_SUBNET_HELP,
            Language.MSG_ADD_DEVICE_HELP,
            Language.MSG_ADD_DESC_HELP,
            Language.MSG_ADD_RADIUS_HELP,
            Language.MSG_ADD_VLAN_HELP,
            Language.MSG_ADD_CHANNEL_HELP,
            Language.MSG_ADD_TYPE_HELP,
            Language.MSG_ADD_OPTION_HELP
        )

    #prompt messages
    YES = "yes"

    #generic statement messages for whole structure
    MSG_APP_WELCOME = "Welcome to Labris Wireless Access Point Controller"
    MSG_APP_CMD_INIT = "Command Line Tool initializing..."
    MSG_ERR_CLASS_INIT_FAILED = '{0} class could not be initialized!'
    MSG_ERR_COMM_INTERFACE_FAILED = "Unknown error occurred while connecting " \
                                    "with communication interface " \
                                    "at %(line)s with detail: %(exception)s"
    MSG_ERR_COMM_INTERFACE_CONNECTED_BUT_FAILED = "Access point connected " \
                                                  "but an unknown error " \
                                                  "occurred while " \
                                                  "executing command : {0}"
    MSG_ERR_ARG_PARSE_GET = "Get_args stopped with an error ({o})"
    MSG_ERR_GENERIC = "An error occurred on line {0} with error:\n{1}"

    #argument parsing while cli statement messages
    MSG_ARG_DESC = 'Use methods below to add, remove, update and ' \
                   'list device(s), ' \
                   'group(s) or config(s) with commands:\n' \
                   'Commands:{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}\n' \
                   '\nOptions:\n{9}\n{10}\n{11}\n{12}\n{13}\n{14}\n{15}\n{16}' \
                   '\n{17}\n{18}\n{19}\n{20}\n{21}\n{22}\n{23}\n{24}\n'

    MSG_CMD_ADD_HELP = "\nUsage:\t$ add [OPTIONS]" \
                       "\n\tAdd device, group, vlan, config etc " \
                       "with given parameters " \
                       "\n\t[-t],[--type]\tDefine \"type\" that should be " \
                       "one of \"device, group, vlan, config\" " \
                       "\n\t[-I],[--ip]\tUse this params when adding " \
                       "some new variables " \
                       "which needs an ip such as device, config, etc." \
                       "\n\t[-n],[--name]\tTo set a name to related " \
                       "type variable " \
                       "\n\t[-b],[--brand]\tTo set device brand to relate " \
                       "with its model and/or firmware" \
                       "\n\t[-m],[--model]\tTo set device model to relate " \
                       "with its config file" \
                       "\n\t[-F],[--firmware]\tTo set device firmware to " \
                       "relate with its config file" \
                       "\n\t[-R],[--relation]\tTo set device relation one " \
                       "of MASTER of SLAVE" \
                       "\n\t[-D],[--description]\tTo set a description to " \
                       "related type variable " \
                       "\n\t[-u],[--username]\tProvide a username which will " \
                       "be used to connect device" \
                       "\n\t[-p],[--password]\tProvide a password which will " \
                       "be used to connect  and configure device"

    MSG_CMD_EDIT_HELP = "\nUsage:\t$ edit [OPTIONS]" \
                        "\n\tEdit details of given type of device with " \
                        "given parameters " \
                        "\n\t[-t],[--type]\tDefine type device, group, " \
                        "vlan, config " \
                        "\n\t[-o],[--option]\tProvide option must be one of " \
                        "related type database fields" \
                        "\n\t[-P],[--param]\tProvide parameter to be " \
                        "update value"

    MSG_CMD_GROUP_HELP = "\nUsage:\t$ group [OPTIONS]" \
                         "\n\tGroup given devices" \
                         "\n\t[-t],[--type]\tDefine type device, group, " \
                         "vlan, config " \
                         "\n\t[-g],[--group]\tDefine the group where given " \
                         "device will be added into" \
                         "\n\t[-i],[--id]\tDefine id of device, group, " \
                         "vlan, config"

    MSG_CMD_SET_HELP = "\nUsage:\t$ set [OPTIONS]" \
                       "\n\tAdd device, group, vlan, config etc with " \
                       "given parameters " \
                       "\n\t[-t],[--type]\tDefine type device, group, " \
                       "vlan, config " \
                       "\n\t[-i],[--id]\tDefine id of device or group" \
                       "\n\t[-o],[--option]\tProvided option must be " \
                       "one of\n\t" \
                       "\"ssid, vlan, channel, frequency, max client, ip\"" \
                       "\n\tThese will be used to gather related commands " \
                       "from config file you provided"

    MSG_CMD_UNSET_HELP = "\nUsage:\t$ unset [OPTIONS]" \
                         "\n\tUnset option, group, vlan, config etc with " \
                         "given parameters " \
                         "\n\t[-t],[--type]\tDefine type device, group, " \
                         "vlan, config " \
                         "\n\t[-i],[--id]\tDefine id of device or group" \
                         "\n\t[-o],[--option]\tProvided option must be " \
                         "one of\n\t" \
                         "\"ssid, vlan, channel, frequency, max client, ip\"" \
                         "\n\tThese will be used to gather related commands " \
                         "from config file you provided"

    MSG_CMD_LIST_HELP = "\nUsage:\t$ ls [OPTIONS]" \
                        "\n\tList details of given type" \
                        "\n\t[-t],[--type]\tList device, group, vlan, config" \
                        "\n\t[-g],[--group]\tList device, vlan or config " \
                        "from given group" \
                        "\n\t[-i],[--id]\tDefine id of group"

    MSG_CMD_SHOW_HELP = "\nUsage:\t$ sh [OPTIONS]" \
                        "\n\tShow details of given type" \
                        "\n\t[-t],[--type]\tDefine type device, group, " \
                        "vlan, config" \
                        "\n\t[-i],[--id]\tDefine id of device or group" \
                        "\n\t[-o],[--option]\tProvided option must be one " \
                        "of\n\t" \
                        "\"ssid, vlan, channel, frequency, max client, ip, " \
                        "cpu, memory, permanent, conf, "

    MSG_CMD_REMOVE_HELP = "\nUsage:\t$ rm [OPTIONS]" \
                          "\n\tShow details of given type" \
                          "\n\t[-t],[--type]\tDefine type device, group, vlan, " \
                          "config and also it can be used such as" \
                          "given type is from to remove a device from a group" \
                          "\n\t[-g],[--group]\tDefine the group where given " \
                          "device will be remove from" \
                          "\n\t[-i],[--id]\tDefine id of device, group, " \
                          "vlan, config"

    MSG_CMD_SELFTEST_HELP = "\nUsage:\t$ self [OPTIONS]" \
                            "\n\tTest by its self with " \
                            "given parameters " \
                            "\n\t[-t],[--type]\tDefine type device, group, " \
                            "vlan, config " \
                            "\n\t[-I],[--ip]\tUse this params when adding " \
                            "some new variables " \
                            "which needs an ip such as device, config, etc." \
                            "\n\t[-n],[--name]\tTo set a name to related " \
                            "type variable " \
                            "\n\t[-D],[--description]\tTo set a description " \
                            "to related type variable " \
                            "\n\t[-u],[--username]\tProvide a username which " \
                            "will be used to connect device"

    MSG_CMD_TAIL_HELP = "\nUsage:\t$ tail [OPTIONS]" \
                        "\n\tTail logs with given parameters " \
                        "\n\t[-f],[--follow]\tFollow provided log file or " \
                        "log database" \
                        "\n\t[-s],[--search]\tUse this params when adding " \
                        "some new variables " \
                        "which needs an ip such as device, config, etc." \
                        "\n\t[-n],[--name]\tTo set a name to related " \
                        "type variable " \
                        "\n\t[-D],[--description]\tTo set a description " \
                        "to related type variable " \
                        "\n\t[-u],[--username]\tProvide a username which " \
                        "will be used to connect device"

    MSG_ADD_ID_HELP = '\t-i,--id\t\t\tProvide ID address to determine ' \
                      'the variable with usage id, always required'

    MSG_ADD_IP_HELP = '\t-I,--ip\t\t\tProvide IP address for the ' \
                      'newly added device ' \
                      'with usage to connect, required while adding or ' \
                      'editing device'

    MSG_ADD_NAME_HELP = '\t-n,--name\t\tProvide a name for the newly ' \
                        'added device with usage name, required when adding'

    MSG_ADD_USERNAME_HELP = '\t-u,--username\t\tProvide username for ' \
                            'the newly added device ' \
                            'with usage username, required when adding'

    MSG_ADD_PASSWORD_HELP = '\t-p,--password\t\tProvide a password for ' \
                            'given username of the newly added device ' \
                            'with usage password, required when adding'

    MSG_ADD_GROUP_HELP = '\t-g,--group\t\Provide an id to the group ' \
                         'with usage group, required when grouping'

    MSG_ADD_CONFIG = '\t-c,--config\t\tAdd new configuration and map it ' \
                     'to the given group or device'

    MSG_ADD_SUBNET_HELP = '\t-S,--subnet\t\tDefine subnet for VLAN will ' \
                          'be configured with usage 255.255.255.0'

    MSG_ADD_DEVICE_HELP = '\t-d,--device\t\tProvide device id to add ' \
                          'provided device to the group'

    MSG_ADD_INTERFACE_HELP = '\t-e,--interface' \
                             '\tProvide an ethernet interface ' \
                             'to configure VLAN for group or device ' \
                             'with usage  eth0'

    MSG_ADD_DESC_HELP = '\t-D,--description\tProvide a short description ' \
                        'for group or device with usage '

    MSG_ADD_RADIUS_HELP = '\t-r,--radius\t\tProvide a Radius id to configure ' \
                          'radius authentication for group or device' \
                          ' with usage radius_id'

    MSG_ADD_SSID_HELP = '\t-S,--ssid\t\tProvide an SSID for group or device ' \
                        'with usage ssid'

    MSG_ADD_VLAN_HELP = '\t-V,--vlan\t\tProvide VLAN id to determine VLAN ' \
                        'for group or device with usage vlan_id'

    MSG_ADD_CHANNEL_HELP = '\t-H,--channel\t\tProvide channel to configure ' \
                           'for group or device with usage channel'

    MSG_ADD_TYPE_HELP = '\t-t,--type\t\tProvide a type of ' \
                        'group/device/config/vlan from database ' \
                        'with usage  group/device/config/vlan ' \
                        'others will cause error(s), always required for all' \
                        'operations'

    MSG_ADD_OPTION_HELP = '\t-o,--option\t\tProvide a type of ' \
                          'group/device/config/vlan from database ' \
                          'with usage group/device/config/vlan, required' \
                          'when set, unset, edit and sh operations'

    MSG_ADD_PARAM_HELP = '\t-P,--param\t\tProvide a parameter ' \
                         'to be set to the given option'

    MSG_ADD_RELATION_HELP = '\t-R, --relation\t\tProvide a relation ' \
                            'to define which device is master and ' \
                            'which device is slave to initialize ' \
                            'the device in inventory'

    MSG_ADD_BRAND_HELP = '\t-b, --brand\t\tProvide a device brand to ' \
                         'identify which model and/or firmware ' \
                         'config file will be loaded to initialize ' \
                         'the device in inventory'

    MSG_ADD_MODEL_HELP = '\t-m, --model\t\tProvide a device model to ' \
                         'identify which config file will be loaded ' \
                         'to initialize the device in inventory'

    MSG_ADD_FIRMWARE_HELP = '\t-F, --firmware\t\tProvide a device firmware to ' \
                            'identify which config file will be loaded ' \
                            'to initialize the device in inventory'

    MSG_ADD_TAIL_FOLLOW_HELP = '\t-f, --follow\t\tFollows streams passing ' \
                               'into given file '

    #newly added variables
    MSG_UPDATE_RECORD = 'Recorded {0} updated with record id {1} and with ' \
                        'name {2}'

    #argument parsing exception error messages
    MSG_ERR_PARSER_EXCEPTION = 'Error occurred on parsing arguments ({0})'
    MSG_ERR_EMPTY_ID = 'Please provide an ID for the {0}:'
    MSG_ERR_EMPTY_IP = 'Please provide an IP for the {0} you would like to add'
    MSG_ERR_EMPTY_NAME = 'Please provide an NAME for the {0} ' \
                         'you would like to add'
    MSG_ERR_EMPTY_DESC = "Please provide a DESCRIPTION for the {0} " \
                         "if you would like to, it is optional"
    MSG_ERR_EMPTY_USERNAME = 'Please provide an USERNAME for the {0}' \
                             ' you would like to add'
    MSG_ERR_EMPTY_PASSWORD = 'Please provide an PASSWORD for the {0}' \
                             ' you would like to add'
    MSG_ERR_EMPTY_CONFIG = 'Please provide an CONFIG id for the {0}' \
                           ' you would like to add'
    MSG_ERR_EMPTY_ID = 'There is no ID has been provided' \
                       'Please make sure you provide an id' \
                       ' with -i, --id usage '
    MSG_ERR_EMPTY_OPTION = 'There is no Option has been provided for ' \
                           'Please make sure you provide an option ' \
                           'with -o, --option usage '

    MSG_ERR_EMPTY_PARAMETER = 'There is no Parameter has been provided ' \
                              'Please make sure you provide an option ' \
                              'with -P, --param usage '

    MSG_ERR_EMPTY_GROUP = "Please provide a group id with usage -g, --group " \
                          "to define which group item will be removed from"

    #config parser statement messages
    MSG_ERR_NO_CONFIG_SECTION = 'No section found in config file' \
                                ' exception ({0})'

    #in/out statement messages
    MSG_ERR_IO_ERROR = "Error occurred while connecting database " \
                       "exception ({0}): {1}"
    MSG_ERR_FILE_BACKUP_FAILED = "Error occurred while backing up " \
                                 "file with exception({0})"
    MSG_ERR_FILE_READ = "Error %(error)s occurred when reading %(file)s"

    #database statement messages
    MSG_ERR_DATABASE_ERROR = 'Unknown error occurred on database commands ' \
                             'with error: (%s)'
    MSG_ERR_DATABASE_INSERT = 'New record could not be inserted into ' \
                              'database. Please try again your command.'

    MSG_ERR_DATABASE_UPDATE = 'Existing record could not be updated'

    MSG_ERR_DATABASE_CONNECT = "An unknown error occurred while connecting " \
                               "database (%s)"
    MSG_ERR_DATABASE_CLOSE = "Connection could not close because of ({0})"

    MSG_ERR_DATABASE_NORECORD = "There is no device record found on table"

    #success statement messages
    MSG_SUCCESS_SELECT = "Getting records from database please wait..."
    MSG_SUCCESS_ADD = "Given values inserted to the database successfully " \
                      "executed. Continue..."
    MSG_SUCCESS_REMOVE = "Record(s) successfully removed from database. " \
                         "Continue..."
    MSG_SUCCESS_UPDATE = "Record(s) successfully updated by given values. " \
                         "Continue..."

    #input prompt messages
    MSG_INPUT_CUSTOM = "Enter parameter for %(custom)s of required device:"
    MSG_INPUT_OPTION = "Enter parameter for %(type)s to execute this command:"
    MSG_INPUT_PARAM_OPTION = "Please enter any %(param)s you would like to set:"

    #execution messages
    MSG_EXE_REQUEST = "Your command(s) will be executing... " \

    #status messages
    MSG_STATUS_ADD_SUCCESS = "New %(type)s added:\n ID: %(id)s\nName:%(name)s"

    #Log server messages
    MSG_LOG_SERVER_CONNECTION_ABORTED = \
        "Connection to Log server has been aborted." \
        "Please check your settings then restart shell"

    MSG_ERR_LOG_SERVER_CONNECTION = \
        "Error occurred while %(command)s Log server: %(exception)s"

    MSG_LOG_SERVER_CONNECT_TRY = "Would you like to try to connect again?(yes):"

    MSG_ERR_ARGUMENT_PROVIDED = "No argument provided to execute command"

    MSG_ERR_TYPE_ARGUMENT_PROVIDED = "No \"type\" provided to execute command"









