#------------------------------------------------------------------------#
# CommandBench - All-purpose application benchmarking tool
# Copyright (C) 2009-2010 Adam Wagner <awagner83@gmail.com>
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

"""
Time handling utilities
"""

from commandbench.cli.helpers import red, green
from datetime import timedelta
from sys import stdout
import re

ISATTY = stdout.isatty()

BEST = 1
WORST = 2

class ParseTimeError: pass

class timedelta(timedelta):

    # Possible values: BEST / WORST / None
    score = None

    @classmethod
    def from_string(cls, timestring):
        # Compile and run regex
        regex = re.compile(r'(?P<minutes>[0-9]+)m(?P<seconds>[0-9]+\.[0-9]+)s')
        match = regex.match(timestring) 
        
        # Error out if no match was found
        if match is None: raise ParseTimeError()

        return cls( minutes=int(match.group('minutes')), 
                seconds=float(match.group('seconds')) )

    def __str__(self):
        string = str((self.days * 60*60*24) 
                + self.seconds + self.microseconds / 1000000.0)
        if ISATTY: 
            if self.score == BEST: return str(green(string))
            elif self.score == WORST: return str(red(string))
            else: return string
        else:
            return string

    def __add__(self, other):
        return timedelta( days = self.days + other.days, 
                seconds = self.seconds + other.seconds,
                microseconds = self.microseconds + other.microseconds )

    def __div__(self, other):
        # Ensure other is float
        other = float(other)
        return timedelta( days = self.days / other, seconds = self.seconds / other,
                microseconds = self.microseconds / other )

