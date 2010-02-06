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

"""Time handling utilities"""

from datetime import timedelta
import re


class ParseTimeError(Exception): 
    """Time could not be parsed from string given."""
    pass


def parsetimedelta(timestring):
    """Return new timedelta instance from a string."""
    # Compile and run regex
    regex = re.compile(r'(?P<minutes>[0-9]+)m(?P<seconds>[0-9]+\.[0-9]+)s')
    match = regex.match(timestring) 
    
    # Error out if no match was found
    if match is None: 
        raise ParseTimeError()

    return timedelta(minutes=int(match.group('minutes')), 
            seconds=float(match.group('seconds')))

