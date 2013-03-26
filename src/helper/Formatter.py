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

@package helper
@date Marh 13, 2013
@author Mike Brown
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/148061
@author Fatih Karatana
@copyright Labris Technology

"""
import cStringIO
import operator


def indent(rows, has_header=False, header_char='-', delim=' | ', justify='left',
           separate_rows=False, prefix='', postfix='', wrapfunc=lambda x: x):
    """
    Indents a table by column.

    @param postfix A string appended to each printed row.
    @param justify Determines how are data justified in their column.
         Valid values are 'left','right' and 'center'.
    @param wrapfunc A function f(text) for wrapping text; each element in
         the table is first wrapped by this function.
    @param delim The column delimiter.
    @param header_char Character to be used for the row separator line
         (if hasHeader==True or separateRows==True).
    @param prefix A string prepended to each printed row.
    @param separate_rows True if rows are to be separated by a line
         of 'headerChar's.
    @param has_header True if the first row consists of the columns' names.
    @param rows A sequence of sequences of items, one sequence per row.

    """

    def row_wrapper(row):
        """
        Wrap rows where delim set

        :param row:
        @return
        """
        new_rows = [str(wrapfunc(item)).split('\n') for item in row]
        return [[substr or '' for substr in item] for item in
                map(None, *new_rows)]

    # break each logical row into one or more physical ones
    logical_rows = [row_wrapper(row) for row in rows]
    # columns of physical rows
    columns = map(None, *reduce(operator.add, logical_rows))
    # get the maximum of each column by the string length of its items
    max_widths = [max([len(str(item)) for item in column])
                  for column in columns]
    row_separator = header_char * (
        len(prefix) + len(postfix) + sum(max_widths) +
        len(delim) * (len(max_widths) - 1))
    # select the appropriate justify method
    justify = {'center': str.center, 'right': str.rjust, 'left': str.ljust}[
        justify.lower()]
    output = cStringIO.StringIO()
    if separate_rows:
        print >> output, row_separator
    for physical_rows in logical_rows:
        for row in physical_rows:
            print >> output, \
                prefix \
                + delim.join([justify(str(item), width) for (item, width) in
                              zip(row, max_widths)]) \
                + postfix
        if separate_rows or has_header:
            print >> output, row_separator
            has_header = False
    return output.getvalue()


def wrap_onspace(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).

    @param width
    @param text
    """
    return reduce(
        lambda line, word, width=width: '%s%s%s' %
                                        (line,
                                         ' \n'[(width <= len(line[line.rfind(
                                             '\n') + 1:]) + len(
                                             str(word).split('\n', 1)[0])
                                         )], word),
        str(text).split(' ')
    )


import re


def wrap_onspace_strict(text, width):
    """
    Similar to wrap_onspace, but enforces the width constraint:
    words longer than width are split.

    @param text
    @param width
    @return Wrapped string to put in a cell

    """
    word_regex = re.compile(r'\S{' + str(width) + r',}')
    return wrap_onspace(
        word_regex.sub(lambda m: wrap_always(m.group(), width), text), width)


import math


def wrap_always(text, width):
    """
    A simple word-wrap function that wraps text on exactly width characters.
    It doesn't split the text in words.

    @param width
    @param text

    @return Always wrapped string to put in a cell for each whitespace
    """
    return '\n'.join([text[width * i:width * (i + 1)]
                      for i in xrange(int(math.ceil(1. * len(text) / width)))])