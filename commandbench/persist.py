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

"""Benchmark Persistance Module"""

import os
import json
import sqlite3
from itertools import groupby


class BenchDB(object):
    """Persist recorded benchmark scores.
    
    Example:
    >>> from os import tmpnam, remove
    >>> dbname = tmpnam()
    >>> db = BenchDB(dbname)
    >>> db.put('/tmp', 'ls', [1, 2, 3])
    >>> db.get('/tmp', 'ls')[1]
    [1, 2, 3]
    >>> remove(dbname)
    """

    def __init__(self, path):
        self.path = path
        if not os.path.isfile(path):
            self.conn = self.setup()
        else:
            self.conn = sqlite3.connect(path)
        
    def setup(self):
        """Setup new persistance db."""
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        try:
            cur.execute("create table benchmarks "
                "(addedon integer, cwd text, command text, result text)")
            cur.execute("create unique index if not exists "
                "benchmark on benchmarks (cwd, command)")
            conn.commit()
        finally:
            cur.close()
        return conn

    def get(self, cwd, command):
        """Get previous benchmark result."""
        cur = self.conn.cursor()
        try:
            cur.execute("select addedon, result from benchmarks "
                "where cwd = ? and command = ?", (cwd, command))
            addedon, result = cur.fetchone()
        finally:
            cur.close()
        return (addedon, json.loads(result))

    def put(self, cwd, command, result):
        """Put new benchmark record."""
        result = json.dumps([str(x) for x in result])

        cur = self.conn.cursor()
        try:
            cur.execute("replace into benchmarks "
                "(addedon, cwd, command, result) "
                "values (datetime(), ?, ?, ?)", (cwd, command, result))
            self.conn.commit()
        finally:
            cur.close()

    def putmany(self, stats):
        """Put many new benchmark results."""
        for stat in stats:
            self.put(stat[0], stat[1], stat[2:])


def stat_list(raw_stats):
    """Extract list of stats to record.
    
    Example:
    >>> list(stat_list([
        ['a', 1, 2, 3],
        ['b', 2, 3, 4],
        ['b', 3, 4, 5]]))
    [['a', 1, 2, 3], ['b', 3, 4, 5]]
    """
    for groupkey, stats in groupby(raw_stats, lambda x: x[0]):
        yield list(stats)[-1]

