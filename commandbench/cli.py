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

from commandbench.about import copyright_line

def init_display(controller, display_options):

    # Check for quite flag
    if display_options['quiet']: return None

    # Build app intro
    intro = "Benchmarking '\x1b[1m{cmd}\x1b[0m' {rep} times (concurrency {concurrency})"

    # Print intro
    print copyright_line, "\n"
    print intro.format( cmd=' '.join(controller.command), rep=controller.repetitions,\
            concurrency=controller.concurrency )
    print "Please be patient...", "\n"
    

def output_results(stats, display_options):

    # Output results
    for type, times in stats.iteritems():
        sum = reduce(lambda x, y: x+y, times)
        avg = sum / len(times)
        print type.ljust(6), 'avg:', avg, 'total:', sum, \
                'min:', min(times), 'max:', max(times)

