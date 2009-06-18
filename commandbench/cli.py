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

from commandbench.about import copyright_line
from functools import partial

COLUMN_WIDTH = '10'

def init_display(controller, display_options):

    # Check for quite flag
    if display_options['quiet']: return None

    # Build app intro
    intro = "Benchmarking command(s) {rep} times (concurrency {concurrency})"

    # Print intro
    print copyright_line, "\n"
    print intro.format( cmd=' and '.join([str(bold(c)) for c in controller.commands]), \
            rep=controller.repetitions,\
            concurrency=controller.concurrency )
    print "Please be patient..."
    

def output_results(command, stats, display_options):

    # What benchmarks should we report
    show = [benchmark.strip() for benchmark in display_options['show'].split(',')]

    print "\n", "results for", bold(command)

    # Output results
    sum = partial(reduce, lambda x, y: x+y)
    values = [(bold(k), sum(v), sum(v)/len(v), min(v), max(v)) for k, v in stats.iteritems()]
    print Table(values,('','AVG','TOTAL','MIN','MAX')).render()

        
class FormattedString(object):

    formatting = None
    value = None

    def __init__(self, formatting, value):
        self.formatting = formatting
        self.value = value

    def __str__(self):
        return ''.join([self.formatting[0],self.value,self.formatting[1]])

    def __getattr__(self, name):
        m = self.value.__getattribute__(name)

        if name in ('capitalize','center','ljust','rjust', 'lower', 
                'lstrip','rstrip','strip','upper'):
            return lambda *args, **kargs: FormattedString(self.formatting, 
                    m(*args,**kargs))
        else:
            return lambda *args, **kargs: m(*args,**kargs)
        
bold = partial(FormattedString, ['\x1b[1m', '\x1b[0m'])

class Table(object):
    
    data = None
    columns = []
    column_width = 10
    border = ''

    def __init__(self,data,columns,column_width=10,border=''):
        self.data = data
        self.columns = columns
        self.column_width = column_width
        self.border = border

    def render(self):
        header = [str(bold(self.row(self.columns)))] 
        return '\n'.join(header + [self.row(r) for r in self.data])

    def row(self, data):
        return self.border.join(
                [str(c.ljust(self.column_width)) for c in 
                    [c if hasattr(c,'ljust') else str(c) for c in data]])

