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

"""Application Process Classes"""

from subprocess import Popen
from os import tmpfile, getcwd, path
from multiprocessing import Pool
from itertools import repeat

from commandbench.time import parsetimedelta
from commandbench.cli import init_display, output_results
from commandbench.persist import BenchDB, stat_list


class Controller:
    """Main process controlling all other process going-ons"""

    def __init__(self, commands, repetitions=1, concurrency=1, 
            display_options=None):
        self.commands = commands
        self.repetitions = repetitions or 1
        self.concurrency = concurrency or 1
        self.display_options = display_options or {}
        self.cwd = getcwd()
        self.dbpath = path.expanduser("~/.commandbench.sqlite3")
        self.db = BenchDB(self.dbpath)


    def run(self):
        """Benchmark process main loop."""
        # Output initial greeting/please wait message
        if self.display_options['quiet'] < 2:
            init_display(self)

        # Run benchmark
        results = []
        progress = lambda x: 100 * (float(x) / len(self.commands))
        try:
            for n, command in enumerate(self.commands):
                if not self.display_options['quiet']:
                    # fetch prev bench time
                    try:
                        addedtime, oldtime = self.db.get(self.cwd, command)
                        print ('benching (%4.1f%%) "%s"...'
                                '\n\tprevious time: %s on %s' 
                                % (progress(n), command, oldtime[0], addedtime))
                    except TypeError:
                        print 'benching (%4.1f%%) "%s"... ' % (progress(n), command)
                results.append(self.run_command(command))
        except KeyboardInterrupt:
            print "\nKeyboard Interrupt Caught... " \
                    "%s benchmarks completed," % len(results),
            if results:
                print "rendering partial result."
            else:
                print "exiting."
                exit(1)

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
                    single_stats.append(parsetimedelta(time))

                stats.append(single_stats)
           
                # build dict of values
                if not labels:
                    labels = single_labels

        output_results(stats, labels, self.display_options) 

        # Record found results
        BenchDB(self.dbpath).putmany([self.cwd] + x for x in stat_list(stats))


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
        finally:
            pool.close()

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


