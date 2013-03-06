# coding=utf-8
__author__ = 'fatih'


class Language(object):
    """
        Language class
    """

    #generic statement messages for whole structure
    MSG_APP_WELCOME = "Welcome to Labris Wireless Access Point Controller"
    MSG_APP_CMD_INIT = "Command Line Tool initializing..."
    MSG_ERR_CLASS_INIT_FAILED = '{0} class could not be initialized!'
    MSG_ERR_COMM_INTERFACE_FAILED = "Unknown error occurred while connecting with communication interface error"
    MSG_ERR_COMM_INTERFACE_CONNECTED_BUT_FAILED = "Access point connected but an unknown error occurred while " \
                                                  "executing command : {0}"
    MSG_ERR_ARG_PARSE_GET = "Get_args stopped with an error ({o})"
    MSG_ERR_GENERIC = "Unknown error occurred on line {0} with error ({1})"

    #argument parsing while cli statement messages
    MSG_ARG_DESC = 'Use methods below to add, remove, update and list device(s), ' \
                   'group(s) or config(s) with commands:\n' \
                   'Commands:\n{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}\n' \
                   '\nOptions:\n{9}\n{10}\n{11}\n{12}\n{13}\n{14}\n{15}\n{16}' \
                   '\n{17}\n{18}\n{19}\n{20}\n{21}\n{22}\n{23}\n{24}\n{25}\n'

    MSG_CMD_ADD_HELP = "\nUsage:\t$ add [OPTIONS]"\
                       "\n\tAdd device, group, vlan, config etc with given parameters " \
                       "\n\t[-t],[--type]\tDefine type device, group, vlan, config " \
                       "\n\t[-I],[--ip]\tUse this params when adding some new variables " \
                       "which needs an ip such as device, config, etc." \
                       "\n\t[-n],[--name]\tTo set a name to related type variable " \
                       "\n\t[-D],[--description]\tTo set a description to related type variable " \
                       "\n\t[-u],[--username]\tProvide a username which will be used to connect device" \
                       "\n\t[-p],[--password]\tProvide a password which will be used to connect  and configure device"

    MSG_CMD_EDIT_HELP = "\nUsage:\t$ edit [OPTIONS]"\
                        "\n\tEdit details of given type of device with given parameters " \
                        "\n\t[-t],[--type]\tDefine type device, group, vlan, config " \
                        "\n\t[-I],[--ip]\tUse this params when adding some new variables " \
                        "which needs an ip such as device, config, etc." \
                        "\n\t[-n],[--name]\tTo set a name to related type variable " \
                        "\n\t[-u],[--username]\tProvide a username which will be used to connect device"

    MSG_CMD_GROUP_HELP = "\nUsage:\t$ group [OPTIONS]" \
                         "\n\tGroup given devices" \
                         "\n\t[-t],[--type]\tDefine type device, group, vlan, config " \
                         "\n\t[-g],[--group]\tDefine the group where given device will be added into" \
                         "\n\t[-I],[--ip]\tUse this params when adding some new variables " \
                         "which needs an ip such as device, config, etc." \
                         "\n\t[-n],[--name]\tTo set a name to related type variable " \
                         "\n\t[-u],[--username]\tProvide a username which will be used to connect device " \
                         "\n\t[-i],[--id]\tDefine id of device, group, vlan, config"

    MSG_CMD_SET_HELP = "\nUsage:\t$ set [OPTIONS]" \
                       "\n\tAdd device, group, vlan, config etc with given parameters " \
                       "\n\t[-t],[--type]\tDefine type device, group, vlan, config " \
                       "\n\t[-i],[--id]\tDefine id of device or group" \
                       "\n\t[-o],[--option]\tProvide option must be one of\n\t" \
                       "\"ssid, vlan, channel, frequency, maxclients, ip, cpu, memory, permanent, conf, " \
                       "firmware, model, serial, clients\"" \
                       "\n\tThese will be used to gather related commands from config file you provided"

    MSG_CMD_UNSET_HELP = "\nUsage:\t$ unset [OPTIONS]" \
                         "\n\tAdd device, group, vlan, config etc with given parameters " \
                         "\n\t[-t],[--type]\tDefine type device, group, vlan, config " \
                         "\n\t[-i],[--id]\tDefine id of device or group" \
                         "\n\t[-o],[--option]\tProvide option must be one of\n\t" \
                         "\"ssid, vlan, channel, frequency, maxclients, ip, cpu, memory, permanent, conf, " \
                         "firmware, model, serial, clients\"" \
                         "\n\tThese will be used to gather related commands from config file you provided"

    MSG_CMD_LIST_HELP = "\nUsage:\t$ ls [OPTIONS]" \
                        "\n\tList details of given type" \
                        "\n\t[-t],[--type]\tAdd device, group, vlan, config "

    MSG_CMD_SHOW_HELP = "\nUsage:\t$ sh [OPTIONS]" \
                        "\n\tShow details of given type" \
                        "\n\t[-t],[--type]\tDefine type device, group, vlan, config"

    MSG_CMD_REMOVE_HELP = "\nUsage:\t$ rm [OPTIONS]" \
                          "\n\tShow details of given type" \
                          "\n\t[-t],[--type]\tDefine type device, group, vlan, config and also it can be used such as" \
                          "given type is from to remove a device from a group" \
                          "\n\t[-g],[--group]\tDefine the group where given device will be remove from" \
                          "\n\t[-i],[--id]\tDefine id of device, group, vlan, config"

    MSG_CMD_SELFTEST_HELP = "\nUsage:\t$ self [OPTIONS]" \
                            "\n\tAdd device, group, vlan, config etc with given parameters " \
                            "\n\t[-t],[--type]\tDefine type device, group, vlan, config " \
                            "\n\t[-I],[--ip]\tUse this params when adding some new variables " \
                            "which needs an ip such as device, config, etc." \
                            "\n\t[-n],[--name]\tTo set a name to related type variable " \
                            "\n\t[-D],[--description]\tTo set a description to related type variable " \
                            "\n\t[-u],[--username]\tProvide a username which will be used to connect device" \

    MSG_ADD_ID_HELP = '\t-i,--id\t\t\tProvide ID address to determine the variable ' \
                      'with usage id'
    MSG_ADD_IP_HELP = '\t-I,--ip\t\t\tProvide IP address for the newly added device ' \
                      'with usage to connect'
    MSG_ADD_NAME_HELP = '\t-n,--name\t\tProvide name for the newly added device with usage name'
    MSG_ADD_USERNAME_HELP = '\t-u,--username\t\tProvide username for the newly added device ' \
                            'with usage username'
    MSG_ADD_PASSWORD_HELP = '\t-p,--password\t\tProvide password for given username of the newly added device ' \
                            'with usage password'
    MSG_ADD_GROUP_HELP = '\t-g,--group\t\tAdd device to the group with usage group '
    MSG_ADD_CONFIG = '\t-c,--config\t\tAdd new configuration and map it to the given group or device'
    MSG_ADD_SUBNET_HELP = '\t-s,--subnet\t\tDefine subnet for VLAN will be configured with usage 255.255.255.0'
    MSG_ADD_DEVICE_HELP = '\t-d,--device\t\tProvide device id to add provided device to the group'
    MSG_ADD_INTERFACE_HELP = '\t-e,--interface\tProvide ethernet interface to configure VLAN for group or device ' \
                             'with usage  eth0'
    MSG_ADD_DESC_HELP = '\t-D,--description\tProvide a short description for group or device with usage '
    MSG_ADD_RADIUS_HELP = '\t-r,--radius\t\tProvide Radius id to configure radius authentication for group or device' \
                          ' with usage radius_id'
    MSG_ADD_SSID_HELP = '\t-S,--ssid\t\tProvide SSID for group or device with usage ssid'
    MSG_ADD_VLAN_HELP = '\t-V,--vlan\t\tProvide VLAN id to determine VLAN for group or device with usage vlan_id'
    MSG_ADD_CHANNEL_HELP = '\t-H,--channel\t\tProvide channel to configure for group or device with usage channel'
    MSG_ADD_FREQ_HELP = '\t-f,--frequency\t\tProvide channel frequency to configure for group or device with usage'
    MSG_ADD_TYPE_HELP = '\t-t,--type\t\tProvide type of group/device/config/vlan from database ' \
                        'with usage  group/device/config/vlan'
    MSG_ADD_OPTION_HELP = '\t-o,--option\t\tProvide type of group/device/config/vlan from database ' \
                          'with usage group/device/config/vlan'

    #newly added variables
    MSG_ADD_NEW = 'A new {0} added with record id {1} and with name {2}'
    MSG_UPDATE_RECORD = 'Recorded {0} updated with record id {1} and with name {2}'

    #argument parsing exception error messages
    MSG_ERR_PARSER_EXCEPTION = 'Error occurred on parsing arguments ({0})'
    MSG_ERR_EMPTY_IP = 'Please provide an IP for the {0} you would like to add'
    MSG_ERR_EMPTY_NAME = 'Please provide an NAME for the {0} you would like to add'
    MSG_ERR_EMPTY_DESC = "Please provide a DESCRIPTION for the {0} if you would like to, it is optional"
    MSG_ERR_EMPTY_USERNAME = 'Please provide an USERNAME for the {0} you would like to add'
    MSG_ERR_EMPTY_PASSWORD = 'Please provide an PASSWORD for the {0} you would like to add'
    MSG_ERR_EMPTY_CONFIG = 'Please provide an CONFIG id for the {0} you would like to add'
    MSG_ERR_EMPTY_ID = 'There is no ID has been provided for the {0} you would like to connect.' \
                       'Please make sure you provide an option with -i, --id usage '
    MSG_ERR_EMPTY_OPTION = 'There is no Option has been provided for the {0} you would like to set.' \
                           'Please make sure you provide an option with -o, --option usage '

    MSG_ERR_EMPTY_PARAMETER = 'There is no Parameter has been provided for the {0} you would like to set.' \
                              'Please make sure you provide an option with -P, --param usage '

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
    MSG_SUCCESS_SELECT = "Retrieving data from database successfully executed. Continue..."
    MSG_SUCCESS_ADD = "Command add successfully executed. Continue..."
    MSG_SUCCESS_REMOVE = "Command rm successfully executed. Continue..."
    MSG_SUCCESS_UPDATE = "Command update successfully executed. Continue..."

