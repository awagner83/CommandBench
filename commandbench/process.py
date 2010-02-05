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

"""Application Process Classes"""

from subprocess import Popen
from os import tmpfile
from multiprocessing import Pool
from itertools import repeat

from commandbench.time import timedelta
from commandbench.cli.interface import init_display, output_results


class Controller:
    """Main process controlling all other process going-ons"""

    def __init__(self, commands, repetitions=1, concurrency=1, 
            display_options=None):
        self.commands = commands
        self.repetitions = repetitions or 1
        self.concurrency = concurrency or 1
        self.display_options = display_options or {}

    def run(self):
        """Benchmark process main loop."""
        # Output initial greeting/please wait message
        init_display(self, self.display_options)

        # Run benchmark
        results = []
        for command in self.commands:
            results.append( self.run_command( command ) )

        # Parse results
        labels = []
        stats = []
        for index, resultset in enumerate(results):
            for result in resultset:
                # Read captured stats
                single_labels = ['command']
                single_stats = [self.commands[index]]
                for stat_line in result.splitlines():
                    try: 
                        stat_type, time = stat_line.split("\t")
                    except ValueError: 
                        continue
                    single_labels.append(stat_type)
                    single_stats.append(timedelta.from_string(time))

                stats.append(single_stats)
           
                # build dict of values
                if not labels:
                    labels = single_labels

        output_results(stats, labels, self.display_options) 


    def run_command(self, command):
        """Run given command with configured reps and concurrency."""
        # Init multi-proc pool & base worker
        pool = Pool(self.concurrency)
        result = pool.map_async(run_command, repeat(command, self.repetitions))

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
    """Create buffer to collect stats for given command."""
    try:
        with tmpfile() as output_buffer:
            with tmpfile() as stats_buffer:
                # Run given command
                Popen('time ' + command, 
                        shell=True, stdout=output_buffer, 
                        stderr=stats_buffer).wait()

                # Read captured stats
                stats_buffer.seek(0)
                result = stats_buffer.read()

        # Return our findings
        return result

    except KeyboardInterrupt:
        return ''

