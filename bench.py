#!/bin/env python
"""
Repeat given command n number of times

usage:
    bench.py n command
    ex: repeat.py 10 ls -al
"""

from subprocess import Popen
from os import tmpfile
import sys

try:
    # Create buffer to collect stats per run
    statsBuffer = tmpfile()
    outputBuffer = tmpfile()

    # Parse command-line opts
    n = int( sys.argv[1] )
    command = sys.argv[2:]

    # Run benchmark
    for i in range( n ):
        # Capture pre-bench file pointer
        start = statsBuffer.tell()

        # Run given command
        Popen( 'time ' + ' '.join(command), 
                shell=True, stdout=outputBuffer, stderr=statsBuffer ).wait()

        # Read captured stats
        statsBuffer.seek(start)
        print statsBuffer.read().splitlines()[2]

    # Close Buffer
    statsBuffer.close()
    
except IndexError:
    print __doc__

