CommandBench -- All-purpose application benchmarking tool
=========================================================================

Running CommandBench
--------------------

You can run CommandBench from this directory with installing:

    ./cb "COMMAND_TO_BENCHMARK" ["COMMAND" ...]

Example:

    $ ./cb -q -n 10 "find $HOME -name '*.py'" "find $HOME | grep .py"

    Benchmarking command(s) 10 times (concurrency 1)
    Please be patient...

    command                           real (avg)       user (avg)       sys (avg)        
    =====================================================================================
    find /home/awagner -name '*.py'   0:00:00.588300   0:00:00.270400   0:00:00.313700   
    find /home/awagner | grep .py     0:00:00.540100   0:00:00.224100   0:00:00.336600   
    =====================================================================================
                                      0:00:00.564200   0:00:00.247250   0:00:00.325150  

Benchmarks can also be run in a xargs-like manner:

    $ cb -q -a "`find . -name "*.py"`" ls   

    Benchmarking command(s) 1 times (concurrency 1)
    Please be patient...

    command                         real (avg)       user (avg)       sys (avg)        
    ===================================================================================
    ls ./commandbench/__init__.py   0:00:00.003000   0:00:00.001000   0:00:00.001000   
    ls ./commandbench/about.py      0:00:00.003000   0:00:00.001000   0:00:00.002000   
    ls ./commandbench/cli.py        0:00:00.003000   0:00:00          0:00:00.002000   
    ls ./commandbench/process.py    0:00:00.003000   0:00:00.001000   0:00:00.001000   
    ls ./commandbench/time.py       0:00:00.003000   0:00:00.001000   0:00:00.004000   
    ls ./setup.py                   0:00:00.003000   0:00:00.001000   0:00:00.001000   
    ===================================================================================
                                    0:00:00.003000   0:00:00.000833   0:00:00.001833   


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
