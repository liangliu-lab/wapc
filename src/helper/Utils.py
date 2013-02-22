# coding=utf-8
"""
    Utils class to handle utility methods
"""
import inspect

__author__ = 'fatih'


class Utils(object):
    """
        Utils class
    """

    def formatter(self, heading, source):
        """
            Format output text as a human readable style

        :param heading:
        :param source:
        """
        try:

            out = ""
            for head in heading:
                out += "| %-20s" % str(head).capitalize() + " "
            out += ' |' + '\n'

            for field in source:
                for s in field:
                    out += "| %-20s" % str(s) + " "
                out += ' |\n'
            out += "\n"
            print out
        except Exception as e:
            print e.message

    def get_line(self):
        """

        :param :self
        :rtype : object
        :return line number:
        """
        return inspect.currentframe().f_back.f_lineno
