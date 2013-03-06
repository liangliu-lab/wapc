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

        :param heading:
        :param source:
        """
        try:

            out = ""
            for head in heading:
                out += "| %-20s" % str(head).capitalize() + " "
            out += ' |' + '\n'
            #self.print_topics(heading, source, 15, 80)

            for field in source:
                 for s in field:
                     out += "| %-20s" % str(s) + " "
                 out += ' |\n'
            out += "\n"
            print out
        except Exception as e:
            print e.message

    def columnize(self, list, displaywidth=80):
        """Display a list of strings as a compact set of columns.

        Each column is only as wide as necessary.
        Columns are separated by two spaces (one was not legible enough).
        """
        if not list:
            self.stdout.write("<empty>\n")
            return
        nonstrings = [i for i in range(len(list))
                      if not isinstance(list[i], str)]
        #if nonstrings:
        #    raise TypeError, ("list[i] not a string for i in %s" %
        #                      ", ".join(map(str, nonstrings)))

        size = len(list)
        if size == 1:
            self.stdout.write('%s\n'%str(list[0]))
            return
            # Try every row count from 1 upwards
        for nrows in range(1, len(list)):
            ncols = (size+nrows-1) // nrows
            colwidths = []
            totwidth = -2
            for col in range(ncols):
                colwidth = 0
                for row in range(nrows):
                    i = row + nrows*col
                    if i >= size:
                        break
                    x = list[i]
                    colwidth = max(colwidth, len(x))
                colwidths.append(colwidth)
                totwidth += colwidth + 2
                if totwidth > displaywidth:
                    break
            if totwidth <= displaywidth:
                break
        else:
            nrows = len(list)
            ncols = 1
            colwidths = [0]
        for row in range(nrows):
            texts = []
            for col in range(ncols):
                i = row + nrows*col
                if i >= size:
                    x = ""
                else:
                    x = list[i]
                texts.append(x)
            while texts and not texts[-1]:
                del texts[-1]
            for col in range(len(texts)):
                texts[col] = texts[col].ljust(colwidths[col])
            self.stdout.write("%s\n"%str("  ".join(texts)))

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


