# coding=utf-8
__author__ = 'fatih'


class Language(object):
    """
        Language class
    """

    def __init__(self):
        Language.MSG_ARG_DESC.format(
            Language.MSG_ADD_IP_HELP,
            Language.MSG_ADD_NAME_HELP,
            Language.MSG_ADD_USERNAME_HELP,
            Language.MSG_ADD_PASSWORD_HELP,
            Language.MSG_ADD_GROUP_HELP,
            Language.MSG_ADD_CONFIG,
            Language.MSG_ADD_SUBNET_HELP,
            Language.MSG_ADD_DEVICE_HELP,
            Language.MSG_ADD_DESC_HELP,
            Language.MSG_ADD_RADIUS_HELP,
            Language.MSG_ADD_SSID_HELP,
            Language.MSG_ADD_VLAN_HELP,
            Language.MSG_ADD_CHANNEL_HELP,
            Language.MSG_ADD_FREQ_HELP
        )

        #generic statement messages for whole structure
    MSG_ERR_CLASS_INIT_FAILED = '{0} class could not be initialized!'
    MSG_ERR_COMM_INTERFACE_FAILED = "Unknown error occurred while connecting with communication interface error"
    MSG_ERR_COMM_INTERFACE_CONNECTED_BUT_FAILED = "Access point connected but an unknown error occurred while executing command : {0}"
    MSG_ERR_ARG_PARSE_GET = "Get_args stopped with an error ({o})"
    MSG_ERR_GENERIC = "Unknown error occurred on line {0} with error ({1})"

    #argument parsing while cli statement messages
    MSG_ARG_DESC = 'Use this method to add device, group or params to devices with commands\n' \
                   '{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}\n{9}\n{10}\n{11}\n{12}\n{13}'
    MSG_ADD_ID_HELP = 'Provide ID address to determine the variable with usage [-id] [--id] [id]'
    MSG_ADD_IP_HELP = 'Provide IP address for the newly added device with usage [-i] [--ip] [192.168.1.1] to connect'
    MSG_ADD_NAME_HELP = 'Set username for the newly added device with usage [-n] [--name] [name]'
    MSG_ADD_USERNAME_HELP = 'Set username for the newly added device with usage [-u] [--username] [username]'
    MSG_ADD_PASSWORD_HELP = 'Set password for given username of the newly added device with usage [-p] [--password] [password]'
    MSG_ADD_GROUP_HELP = 'Add device to the group with usage [-g] [--group] [group] '
    MSG_ADD_CONFIG = 'Add new configuration and map it to the given group or device with [-c] [--config] [config_id]'
    MSG_ADD_SUBNET_HELP = 'Define subnet for VLAN will be configured with usage [-s] [--subnet] [255.255.255.0]'
    MSG_ADD_DEVICE_HELP = 'Set device id to add provided device to the group with usage [-d] [--device] [device_id]'
    MSG_ADD_INTERFACE_HELP = 'Set ethernet interface to configure VLAN for group or device with usage [-inet] [--interface] [eth0]'
    MSG_ADD_DESC_HELP = 'Provide a short description for group or device with usage [-desc] [--description] [eth0]'
    MSG_ADD_RADIUS_HELP = 'Set Radius id to configure radius authentication for group or device with usage [-r] [--radius] [radius_id]'
    MSG_ADD_SSID_HELP = 'Set SSID for group or device with usage [-sid] [--ssid] [ssid]'
    MSG_ADD_VLAN_HELP = 'Set VLAN id to determine VLAN for group or device with usage [-vid] [--vlan] [vlan_id]'
    MSG_ADD_CHANNEL_HELP = 'Set channel to configure for group or device with usage [-ch] [--channel] [channel]'
    MSG_ADD_FREQ_HELP = 'Set channel frequency to configure for group or device with usage [-fq] [--frequency] [freq]'
    MSG_ADD_TYPE_HELP = 'Set type of group/device/config/vlan from database with usage [-t] [--type] [group/device/config/vlan]'

    #newly added variables
    MSG_ADD_NEW = 'A new {0} added with record id {1} and with name {2}'

    #argument parsing exception error messages
    MSG_ERR_PARSER_EXCEPTION = 'Error occurred on parsing arguments ({0})'
    MSG_ERR_EMPTY_IP = 'Please provide an IP for the {0} you would like to add'
    MSG_ERR_EMPTY_NAME = 'Please provide an NAME for the {0} you would like to add'
    MSG_ERR_EMPTY_USERNAME = 'Please provide an USERNAME for the {0} you would like to add'
    MSG_ERR_EMPTY_PASSWORD = 'Please provide an PASSWORD for the {0} you would like to add'
    MSG_ERR_EMPTY_CONFIG = 'Please provide an CONFIG id for the {0} you would like to add'

    #config parser statement messages
    MSG_ERR_NO_CONFIG_SECTION = 'No section found in config file exception ({0})'


    #in/out statement messages
    MSG_ERR_IO_ERROR = "Error occurred while connecting database exception ({0}): {1}"
    MSG_ERR_FILE_BACKUP_FAILED = "Error occurred while backing up file with exception({0})"

    #database statement messages
    MSG_ERR_DATABASE_ERROR = 'Unknown error occurred on {0} line while {1} database with error: ({2})'
    MSG_ERR_DB_CONNECT = "An unknown error occurred while connecting database ({0})"
    MSG_ERR_DB_CLOSE = "Connection could not close because of ({0})"

    #success statement messages
    MSG_SUCCESS_SELECT = "Command ls successfully executed. Continue..."
    MSG_SUCCESS_ADD = "Command add successfully executed. Continue..."
    MSG_SUCCESS_REMOVE = "Command rm successfully executed. Continue..."
    MSG_SUCCESS_UPDATE = "Command update successfully executed. Continue..."

