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
#
import wpipe

pserver = wpipe.Server('mypipe', wpipe.Mode.Slave)
while True:
    for client in pserver:
        while client.canread():
            rawmsg = client.read()
            client.write(b'hallo')    
    pserver.waitfordata()
pserver.shutdown()

pclient = wpipe.Client('mypipe', wpipe.Mode.Master)
while True:
    pclient.write(b'hello')
    reply = pclient.read()
pclient.close()
