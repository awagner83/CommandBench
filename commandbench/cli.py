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

"""CLI Output Methods."""

from functools import partial

from datagrid.core import DataGrid
from datagrid.renderer import ascii


def init_display(controller):
    """Welcome/Startup output."""

    # Print intro
    print ("Benchmarking command(s) %s times (concurrency %s)" %
            (controller.repetitions, controller.concurrency))
    print "Please be patient..."
    

def output_results(stats, labels, display_options):
    """Output results table."""

    # Columns are all averages, reflect in labels
    labels[1:] = ["%s (avg)" % label for label in labels[1:]]

    # Aggregate Methods
    time_sum = partial(reduce, lambda x, y: x+y)
    average = lambda vals: time_sum(vals) / len(vals)

    # Setup DataGrid
    grid = DataGrid(stats, labels, 
        aggregate=dict((label, average) for label in labels[1:]),
        groupby=['command'], suppressdetail=True)
    print "\n", grid.render(ascii.Renderer())

