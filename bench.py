#!/bin/env python
"""
Repeat given command n number of times

usage:
    repeat.py n command
    ex: repeat.py 10 ls -al
"""

import subprocess
import sys
import os

output = open('output','w+')

try:
    n = int( sys.argv[1] )
    command = sys.argv[2:]
    for i in range( n ): 
        subprocess.Popen( 'time ' + ' '.join(command), 
                shell='sh', stderr=output )
except IndexError:
    print __doc__

