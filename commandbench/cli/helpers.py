#------------------------------------------------------------------------#
# CommandBench - All-purpose application benchmarking tool
# Copyright (C) 2009 Adam Wagner <awagner83@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------#

from functools import partial
from sys import stdout

ISATTY = stdout.isatty()

class FormattedString(object):
    """
    ANSI Escape Sequence "Formatted String Factory"
    """

    formatting = None
    value = None

    def __init__(self, formatting, value):
        self.formatting = formatting
        self.value = value

    def __str__(self):
        if ISATTY:
            return ''.join([self.formatting[0],self.value,self.formatting[1]])
        else: return self.value
    
    def __getattr__(self, name):
        m = self.value.__getattribute__(name)
        
        def string_method(method, fmt, *args, **kargs):
            result = method(*args,**kargs)
            if type(result) == str: return FormattedString(fmt,result)
            else: return result

        return partial( string_method, m, self.formatting )


bold = partial(FormattedString, ['\x1b[1m', '\x1b[0m'])

class Table(object):
    """
    Fixed-width ascii table
    """
    
    data = None
    columns = []
    column_width = 10
    border = ''

    def __init__(self,data,columns=[],column_width=10,border=''):
        self.data = data
        self.columns = columns
        self.column_width = column_width
        self.border = border

    def render(self):
        """
        Generate table from given init data and return
        """
        header = [str(bold(self.row(self.columns)))] 
        return '\n'.join(header + [self.row(r) for r in self.data])

    def row(self, data):
        """
        Generate row to be injected in final rendered table
        """
        return self.border.join(
                [str(c.ljust(self.column_width)) for c in 
                    [c if hasattr(c,'ljust') else str(c) for c in data]])

