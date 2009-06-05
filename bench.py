#!/bin/env python
#------------------------------------------------------------------------#
# CommandBench - All-purpose command-line application benchmarking tool
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

"""
Command-line application benchmarking software

usage:
    bench.py n command
    ex: repeat.py 10 ls -al
"""

from subprocess import Popen
from os import tmpfile
from pprint import pprint
import sys

try:
    # Create buffer to collect stats per run
    statsBuffer = tmpfile()
    outputBuffer = tmpfile()

    # Parse command-line opts
    n = int( sys.argv[1] )
    command = sys.argv[2:]

    # Init stat storage
    stats = {}

    # Run benchmark
    for i in range( n ):
        # Capture pre-bench file pointer
        start = statsBuffer.tell()

        # Run given command
        Popen( 'time ' + ' '.join(command), 
                shell=True, stdout=outputBuffer, stderr=statsBuffer ).wait()

        # Read captured stats
        statsBuffer.seek(start)
        for statLine in statsBuffer.read().splitlines():
            try: type, time = statLine.split("\t")
            except: continue

            try: stats[type][0]
            except: stats[type] = []
            stats[type].append(time)

    pprint( stats )

    # Close Buffer
    statsBuffer.close()
    
except IndexError:
    print __doc__

