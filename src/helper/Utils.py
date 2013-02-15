# coding=utf-8
import inspect

__author__ = 'fatih'


class Utils(object):
    """
        Utils class
    """

    def formatter(self, stream):
        """
            Format output text as a human readable style
        :param stream:
        """

    def get_line(self):
        """

        :param :self
        :rtype : object
        :return line number:
        """
        return inspect.currentframe().f_back.f_lineno
