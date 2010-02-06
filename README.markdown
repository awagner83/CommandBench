CommandBench -- All-purpose application benchmarking tool
=========================================================================

Running CommandBench
--------------------

You can run CommandBench from this directory with installing:

    ./cb "COMMAND_TO_BENCHMARK" ["COMMAND" ...]

Example:

    $ ./cb -n 10 "find $HOME -name '*.py'" "find $HOME | grep .py"

    This is CommandBench v0.3b, http://github.com/awagner83/CommandBench/
    Copyright (C) 2009 Adam Wagner <awagner83@gmail.com> 

    Benchmarking command(s) 10 times (concurrency 1)
    Please be patient...

    command                           real             user             sys              
    =====================================================================================
    find /home/awagner -name '*.py'   0:00:00.588300   0:00:00.270400   0:00:00.313700   
    find /home/awagner | grep .py     0:00:00.540100   0:00:00.224100   0:00:00.336600   
    =====================================================================================
                                      0:00:00.564200   0:00:00.247250   0:00:00.325150  


Dependencies
------------

*   Python 2.6
*   DataGrid 0.1

Installing CommandBench
-----------------------

For a system-wide installation run (as root):

    ./setup.py install


CommandBench is licensed under the GNU/GPLv3 (see COPYING for details).

Copyright (C) 2009-2010 Adam Wagner <awagner83@gmail.com>
