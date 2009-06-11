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
from multiprocessing import Pool
from commandbench.time import parsetime
from commandbench.about import copyright_line

class Controller:
    """
    Main process controlling all other process going-ons
    """

    # Command to be benchmarked
    command = None

    # Number of times to run benchmark
    repetitions = 1

    # Concurrency level
    concurrency = 1

    def __init__(self, command, repetitions=1, concurrency=1):
        self.command = command
        self.repetitions = repetitions
        self.concurrency = concurrency

    def run(self):
        # Init stat storage
        stats = {}

        # Init multi-proc pool & base worker
        pool = Pool(self.concurrency)

        # Output app intro
        print copyright_line, "\n"
        print "Benchmarking", "'"+' '.join(self.command)+"'", \
            self.repetitions, "times."
        print "Please be patient...", "\n"

        # Run benchmark
        for result in pool.map(run_command, [self.command for x in range(self.repetitions)]):
            # Read captured stats
            for statLine in result.splitlines():
                try: type, time = statLine.split("\t")
                except: continue

                try: stats[type][0]
                except: stats[type] = []
                stats[type].append(parsetime(time))

        # Output results
        for type, times in stats.iteritems():
            sum = reduce(lambda x, y: x+y, times)
            print type.ljust(6), 'avg:', sum / len(times), '  total:', sum


def run_command(command):
    # Create buffer to collect stats per run
    statsBuffer = tmpfile()
    outputBuffer = tmpfile()

    # Run given command
    Popen( 'time ' + ' '.join(command), 
            shell=True, stdout=outputBuffer, stderr=statsBuffer ).wait()

    # Read captured stats
    statsBuffer.seek(0)
    result = statsBuffer.read()

    # Close temp files
    statsBuffer.close()
    outputBuffer.close()

    # Return our findings
    return result

