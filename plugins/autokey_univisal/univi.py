from tempfile import gettempdir
from multiprocessing import Process as Process_mp
# from os import open as os_open
# from os import O_RDONLY, O_NONBLOCK

readpipe = gettempdir() + '/univisal.out.fifo'
writepipe = gettempdir() + '/univisal.in.fifo'

key = engine.get_macro_arguments()[0]
if key is None:
    key = ""
    exit(1)

def univi():
    # Opening pipes blocks until the other end is connected to.
    outpt = open(writepipe, "w")
    outpt.write(key)
    outpt.close()
    outpt = open(readpipe, "r")
    # outpt = os_open(readpipe, O_RDONLY|O_NONBLOCK)
    output = outpt.read()
    outpt.close()
    if output != "nop":
        engine.set_return_value(output)

univi()

# exit(1)
# # Start univi as a process
# p = Process_mp(target=univi)
# p.start()
# # Wait for n seconds or until process finishes
# p.join(0.5)
# if p.is_alive():
#     print("Univi timed out. Is univisal reading from {}?".format(readpipe))
#     engine.set_return_value(key)
#     p.terminate()
#     p.join()
