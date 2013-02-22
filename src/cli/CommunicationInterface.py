# coding=utf-8
import io
import json
import os
import subprocess
from src.language.language import Language
from src.resources.resources import Resources

__author__ = 'fatih'


class CommunicationInterface(object):
    """
        Communication interface class to talk with perl script
    """

    def get_source_config(self, file):
        """
            Get input json file to parse with params
        :param file: 
        """
        try:
            f = open(file, 'r')
            config_source = f.read()
            f.close()
            return config_source
        except Exception as e:
            print e.message
            pass

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
        except Exception as e:
            print Language.MSG_ERR_COMM_INTERFACE_FAILED.format(e.message)
            pass

    def write_source_file(self, source):
        """
            Write source file to provide the communication interface
        :param source: 
        """
        try:
            f = open(Resources.ci_source, 'w+')
            f.write(json.dumps(source))
            f.close()
        except Exception as e:
            print e.message
            pass

    def backup(self, source, target, time):
        """

        :rtype : object
        :param source: 
        :param target: 
        :param time: 
        """
        try:
            backup_folder = Resources.BACKUP_PATH + target
            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)
            f = open(backup_folder + "/" + Resources.back_name.format(time.replace(' ', '-')), 'w+')
            f.write(json.dumps(source))
            f.close()
        except Exception as e:
            print Language.MSG_ERR_FILE_BACKUP_FAILED.format(e.message)
            pass


