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

"""CLI Output Methods."""

from commandbench.about import copyright_line
from commandbench.cli.helpers import bold
from functools import partial

from datagrid.core import DataGrid
from datagrid.renderer import ascii


def init_display(controller, display_options):
    """Welcome/Startup output."""

    # Check for quite flag
    if display_options['quiet']: 
        return None

    # Build app intro
    intro = "Benchmarking command(s) {rep} times (concurrency {concurrency})"

    # Print intro
    print copyright_line, "\n"
    print intro.format( cmd=' and '.join([str(bold(c)) 
        for c in controller.commands]), \
            rep=controller.repetitions,\
            concurrency=controller.concurrency )
    print "Please be patient..."
    

def output_results(stats, labels, display_options):
    """Output results table."""

    # Aggregate Methods
    time_sum = partial(reduce, lambda x, y: x+y)
    average = lambda vals: time_sum(vals) / len(vals)

    # Setup DataGrid
    grid = DataGrid(stats, labels, 
        aggregate={"real": average, "user": average, "sys": average},
        groupby=['command'], suppressdetail=True)
    print "\n", grid.render(ascii.Renderer())

