#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import socket
from threading import Thread
import sys

PORT = 10000
HOST = '127.0.0.1'

global mode
mode = 'test'

def handleKey(key):
    if key == "m":
        return "l"
    elif key == "d":
        return "d"
    else:
        return key

MAX_LENGTH = 1024
def handle(clientsocket):
  # sys.stdout.write("hi")
  while True:
    buf = clientsocket.recv(MAX_LENGTH)
    # if buf == '': return #client terminated connection
    # We only handle one key at a time. Several characters is bad input.
    if len(buf) != 1: return
    # TODO: make modes enum.
    if mode == "insert":
        print(buf)
        clientsocket.send(buf)
    else:
        output = handleKey(buf)
        print(output)
        clientsocket.send(output)
    return

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind((HOST, PORT))
serversocket.listen(10)
while 1:
    #accept connections from outside
    (clientsocket, address) = serversocket.accept()
    ct = Thread(target=handle, args=(clientsocket,))
    ct.start()
