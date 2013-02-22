# coding=utf-8
__author__ = "fatih"
__date__ = "$Jan 22, 2013 11:08:40 AM$"


class Resources(object):
    """
        Resources file covers all required global variables, pathnames, filenames, etc.
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

    #global device config file resource
    cfg_device_resource = CONFIG_PATH + "wapc_config.json"

    #database config file
    __db__config__ = CONFIG_PATH + "database.cfg"

    #backup file name
    back_name = "backup-{0}.bak"

    #shell initial prompt
    prompt = "WACP:~ cli$ "

    #global recent time format
    time_format = "%Y-%m-%d %H:%M:%S"

    #config file variables for postgresql
    cfg_section_postgre = "postgre"

    #config file variables for mysql
    cfg_section_mysql = "mysql"

    #column headers for files
    headers = {'device' : '',
               'group': {'ID', 'Name', 'Description', 'Configuration ID', 'Add Date', 'Last Modify'}}