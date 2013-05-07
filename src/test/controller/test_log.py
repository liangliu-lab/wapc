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

@package test
@date Marh 13, 2013
@author Fatih Karatana
@author <a href="mailto: fatih@karatana.com">fatih@karatana.com</a>
@copyright Labris Technology

"""

from src.controller.Logger import Logger
from src.model.Log import Log
import unittest

__author__ = 'fatih'


class LogTestCase(unittest.TestCase):
    def test_logger(self):
        self.assertIn()
        my_logger = Logger()
        log_id = my_logger.create_log(
            'Test Log',
            Log.severity.DEBUG,
            my_logger.utils.get_line(),
            'Logger test message',
            'create_log',
            'facility',
            'localhost')
        print "New log created with id: " + log_id

        print my_logger.gather_logs(None, '_all_docs')

if __name__ == '__main__':
    test_logger = LogTestCase()
    test_logger.test_logger()
