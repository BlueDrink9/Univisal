# import win32pipe
# import win32file
# pipename = r'\\.\pipe\univisal'
# # pipename should be of the form \\.\pipe\mypipename
# pipe = win32pipe.CreateNamedPipe(
#         pipename,
#         win32pipe.PIPE_ACCESS_OUTBOUND,
#         win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
#         1, 65536, 65536,
#         300,
#         None)
# try:
#     win32pipe.ConnectNamedPipe(pipe, None)

#     while True:
#         some_data = b'12345...'
#         win32file.WriteFile(pipe, some_data)
#         ...
# finally:
#     win32file.CloseHandle(pipe)
import sys, os
from win32file import *
# try to open WinUAE pipe, or exit
try:
  up = CreateFile(r'\\.\pipe\WinUAE', GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, None)
except Exception as e:
  print("Can't open WinUAE pipe.")
  print(e)
  sys.exit(-1)
# join all command line args (except scriptname)
args = " ".join(sys.argv[1:]) + "\0"
# write args to WinUAE pipe
WriteFile(up, args)
# output return code
print(ReadFile(up, 4096)[1])
# close handle
CloseHandle(up)

exit()
import wpipe

pserver = wpipe.Server('mypipe', wpipe.Mode.Slave)
while True:
    for client in pserver:
        while client.canread():
            rawmsg = client.read()
            print(rawmsg)
            client.write(b'hallo')
    pserver.waitfordata()
pserver.shutdown()

pclient = wpipe.Client('mypipe', wpipe.Mode.Master)
while True:
    pclient.write(b'hello')
    reply = pclient.read()
pclient.close()
