#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import socket
from threading import Thread
import sys
import os
# Available since 3.1
# import importlib
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

from handleKey import *

PORT = 10000
HOST = '127.0.0.1'

MAX_LENGTH = 1024

def close(sock):
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

def handle(clientsocket):
  while True:
    buf = clientsocket.recv(MAX_LENGTH).decode()
    # if buf == '': return #client terminated connection
    if buf == "HUP":
        close(serversocket)
        # Doesn't work in multithreaded environment.
        sys.exit(0)
        # close(serversocket)
    # We only handle one key at a time. Several characters is bad input.
    # if len(buf) != 1: return
    output = handleKey(buf)
    print(output)
    clientsocket.send(output.encode())
    return

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind((HOST, PORT))
# Allow instant reuse of socket if program closed.
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.listen(10)
while True:
    #accept connections from outside
    (clientsocket, address) = serversocket.accept()
    ct = Thread(target=handle, args=(clientsocket,))
    ct.start()
