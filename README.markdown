CommandBench -- All-purpose application benchmarking tool
=========================================================================

Running CommandBench
--------------------

You can run CommandBench from this directory with installing:

    ./cb "COMMAND_TO_BENCHMARK" ["COMMAND" ...]

Example:

    $ ./cb -n 50 \
        "find . -name '*pyc*'" \
        "find . -name '*pyc'" \
        "find . | grep pyc"

    This is CommandBench v0.3b, http://github.com/awagner83/CommandBench/
    Copyright (C) 2009 Adam Wagner <awagner83@gmail.com>

    Benchmarking command(s) 50 times (concurrency 1)
    Please be patient...

    command                  real      user      sys
    =======================================================
    find ../ -name '*pyc'    0.07432    0.0241      0.05
    find ../ -name '*pyc*'   0.07416    0.0242   0.04976
    find ../ | grep pyc      0.06932   0.01908   0.05264
    =======================================================
                              0.0726   0.02246    0.0508


Dependencies
------------

*   Python 2.6
*   DataGrid 0.1

Installing CommandBench
-----------------------

For a system-wide installation run (as root):

    ./setup.py install


CommandBench is licensed under the GNU/GPLv3 (see COPYING for details).

Copyright (C) 2009 Adam Wagner <awagner83@gmail.com>
