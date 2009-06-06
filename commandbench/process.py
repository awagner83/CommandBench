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
Application Process Classes
"""

from subprocess import Popen
from os import tmpfile
from pprint import pprint
from commandbench.time import parsetime

class Controller:
    """
    Main process controlling all other process going-ons
    """

    # Command to be benchmarked
    command = None

    # Number of times to run benchmark
    repetitions = 0

    def __init__(self, command, repetitions):
        self.command = command
        self.repetitions = repetitions

    def run(self):
        # Create buffer to collect stats per run
        statsBuffer = tmpfile()
        outputBuffer = tmpfile()

        # Init stat storage
        stats = {}

        print "This is CommandBench, http://github.com/awagner83/CommandBench/"
        print "Copyright (C) 2009 Adam Wagner <awagner83@gmail.com>", "\n"
        print "Benchmarking", "'"+' '.join(self.command)+"'", \
            self.repetitions, "times."
        print "Please be patient...", "\n"

        # Run benchmark
        for i in range( self.repetitions ):
            # Capture pre-bench file pointer
            start = statsBuffer.tell()

            # Run given command
            Popen( 'time ' + ' '.join(self.command), 
                    shell=True, stdout=outputBuffer, stderr=statsBuffer ).wait()

            # Read captured stats
            statsBuffer.seek(start)
            for statLine in statsBuffer.read().splitlines():
                try: type, time = statLine.split("\t")
                except: continue

                try: stats[type][0]
                except: stats[type] = []
                stats[type].append(parsetime(time))

        # Output results
        for type, times in stats.iteritems():
            sum = reduce(lambda x, y: x+y, times)
            print type.ljust(6), 'avg:', sum / len(times), '  total:', sum

        # Close Buffer
        statsBuffer.close()

