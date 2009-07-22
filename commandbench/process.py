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

"""
Application Process Classes
"""

from subprocess import Popen
from os import tmpfile
from pprint import pprint
from multiprocessing import Pool
from commandbench.time import timedelta, BEST, WORST
from commandbench.cli.interface import init_display, output_results
from collections import defaultdict
from functools import partial
from itertools import chain

class Controller:
    """
    Main process controlling all other process going-ons
    """

    # Command to be benchmarked
    commands = None

    # Number of times to run benchmark
    repetitions = 1

    # Concurrency level
    concurrency = 1

    # Display options
    display_options = {}

    def __init__(self, commands, repetitions=1, concurrency=1, 
            display_options={}):
        self.commands = commands
        self.repetitions = repetitions if repetitions else 1
        self.concurrency = concurrency if concurrency else 1
        self.display_options = display_options

    def run(self):
        # Output initial greeting/please wait message
        init_display(self, self.display_options)

        # Run benchmark
        results = []
        for command in self.commands:
            results.append( self.run_command( command ) )

        # Parse results
        all_stats = []
        sum = partial(reduce, lambda x, y: x+y)
        for index, resultset in enumerate(results):
            # Init stat storage
            stats = defaultdict(list)

            for result in resultset:
                # Read captured stats
                for statLine in result.splitlines():
                    try: type, time = statLine.split("\t")
                    except: continue

                    stats[type].append(timedelta.from_string(time))
           
            # build dict of values
            values = [(k, sum(v), sum(v)/len(v), min(v), max(v))
                    for k, v in stats.iteritems()]

            # append to list of all stats
            all_stats.append(values)

        # Mark max/min values
        print [x for x in chain(*all_stats)]

        exit()
        for values in chain(*[x[1:] for x in all_stats]): 
            min(values).score = BEST
            max(values).score = WORST

        # Output results
        for stats in all_stats: 
            output_results(self.commands[index], stats, self.display_options)


    def run_command(self, command):
        # Init multi-proc pool & base worker
        pool = Pool(self.concurrency)
        result = pool.map_async(run_command, \
                [command for x in range(self.repetitions)])

        # Wait for results
        try:
            while True:
                result.wait(0.25)
                if result.ready(): 
                    results = result.get()
                    break
        except KeyboardInterrupt:
            print "\nKeyboard Interrupt Caught. Terminating benchmark..."
            pool.close()
            exit(1)

        return results


def run_command(command):
    # Create buffer to collect stats per run
    try:
        with tmpfile() as outputBuffer:
            with tmpfile() as statsBuffer:
                # Run given command
                Popen( 'time ' + command, 
                        shell=True, stdout=outputBuffer, stderr=statsBuffer ).wait()

                # Read captured stats
                statsBuffer.seek(0)
                result = statsBuffer.read()

        # Return our findings
        return result

    except KeyboardInterrupt:
        return ''

