#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# This is just a thin CLI tool to interact with univisal.py.
# Usage: univi.py [key]
# Takes only a single argument.
import socket
import sys


HOST = '127.0.0.1'
PORT = 10000
s = socket.socket()
s.connect((HOST, PORT))

import sys
# print "This is the name of the script: ", sys.argv[0]
# print "Number of arguments: ", len(sys.argv)
# print "The arguments are: " , str(sys.argv)
if len(sys.argv) != 2:
    print("Usage: univi.py [key]")
    sys.exit(1)
# print "The arguments are: " , str(sys.argv)
s.send(str(sys.argv[1]))
s.close()
sys.exit(0)
