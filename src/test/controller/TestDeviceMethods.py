from src.controller.DeviceMethods import DeviceMethods

__author__ = 'fatih'

import unittest


class TestDeviceMethods(unittest.TestCase):
    def test_get_file_list(self):
        from argparse import Namespace
        params = Namespace()
        device_methods = DeviceMethods(params)
        print device_methods.get_device_list()


if __name__ == '__main__':
    unittest.main()
