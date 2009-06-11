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

def init_display(controller):

    # Output app intro
    print copyright_line, "\n"
    print "Benchmarking", "'"+' '.join(controller.command)+"'", \
        controller.repetitions, "times (concurrency level", \
        str(controller.concurrency) + ")"
    print "Please be patient...", "\n"
    

def output_results(stats):

    # Output results
    for type, times in stats.iteritems():
        sum = reduce(lambda x, y: x+y, times)
        print type.ljust(6), 'avg:', sum / len(times), '  total:', sum

