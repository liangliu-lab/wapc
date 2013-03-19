# coding=utf-8
"""
    Utils class to handle utility methods
"""
import inspect
import re
from src.resources.resources import Resources

__author__ = 'fatih'


class Utils(object):
    """
        Utils class
    """
    def getCleanParams(self, args):
        """

        :param args:
        :return:
        """
        regex = re.compile("\-\S*[^\-]*", re.IGNORECASE)
        arglist = regex.findall(args)
        return arglist

    def formatter(self, heading, source):
        """
            Format output text as a human readable style

        :param heading list
        :param source is a tuple list
        """
        import formatter
        try:
            width = 30
            head = [str(i).replace("_"," ").upper() for i in heading]
            print formatter.indent([head]+source, hasHeader=True, separateRows=True,
                             prefix='| ', postfix=' |',
                             wrapfunc=lambda x: formatter.wrap_onspace(x,width))
        except Exception as e:
            print e.message

    def get_line(self):
        """
            Get current line of file to handle exception lines
        :param :self
        :rtype : object
        :return line number:
        """
        return inspect.currentframe().f_back.f_lineno

    def validate(self, source=None, stype=None):
        """
        This method is used to validate given input source by type format such as IP,
        email, whitespace-fress strings, etc.

        :param stype: type defines what sort of value will be validated.
        Recently supported keys name, eth & ip
        :param source:
        """
        src = ''.join(source.split())
        regex = re.compile(Resources.REGEX[stype], re.IGNORECASE)
        arg = ''.join(regex.findall(src))
        return arg


