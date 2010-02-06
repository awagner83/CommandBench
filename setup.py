#!/usr/bin/env python
#------------------------------------------------------------------------#
# CommandBench - All-purpose command-line application benchmarking tool
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

from distutils.core import setup
from commandbench import about

setup(  name = about.name,
        version = about.version,
        author = about.author,
        author_email = about.email,
        url = about.website,
        description = about.description,
        license = about.license,
        packages = ['commandbench', 'commandbench.cli'],
        data_files = [('bin', ['cb'])],
        classifiers = ['Programming Language :: Python',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Environment :: Console',
            'Intended Audience :: Developers']
     )


