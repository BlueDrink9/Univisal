from tempfile import gettempdir
# from os import open as os_open
# from os import O_RDONLY, O_NONBLOCK

readpipe = gettempdir() + '/univisal.out.fifo'
writepipe = gettempdir() + '/univisal.in.fifo'

key = engine.get_macro_arguments()[0]
if key is None:
    key = ""
outpt = open(writepipe, "w")
outpt.write(key)
outpt.close()
outpt = open(readpipe, "r")
# outpt = os_open(readpipe, O_RDONLY|O_NONBLOCK)
output = outpt.read()
outpt.close()
if output != "nop":
    engine.set_return_value(output)
