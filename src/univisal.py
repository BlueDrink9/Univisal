#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import socket
from threading import Thread


MAX_LENGTH = 4096

def handle(clientsocket):
  while 1:
    buf = clientsocket.recv(MAX_LENGTH)
    # if buf == '': return #client terminated connection
    # We only handle one key at a time. Several characters is bad input.
    if len(buf) != 1: return
    # Todo: make enum.
    if mode == "insert":
        return buf
    else:
        handleKey(buf)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 10000
HOST = '127.0.0.1'

serversocket.bind((HOST, PORT))
serversocket.listen(10)

while 1:
    #accept connections from outside
    (clientsocket, address) = serversocket.accept()

    ct = Thread(target=handle, args=(clientsocket,))
    ct.start()

def handleKey(key):
    if key == "m":
        return "l"
    elif key == "d":
        return "d"
    else:
        return key