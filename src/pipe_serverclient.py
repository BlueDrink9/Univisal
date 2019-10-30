import time
import sys
import pywintypes, win32pipe, win32file

pipename=r'\\.\pipe\mypipe'

def pipe_server():
    print("pipe server")
    pipe = win32pipe.CreateNamedPipe(
        pipename,
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None)
    try:
        print("waiting for client")
        win32pipe.ConnectNamedPipe(pipe, None)
        print("got client")

        count = 0
        while count < 5:
            print(f"writing message {count}")
            # convert to bytes
            some_data = str.encode(f"count {count}")
            win32file.WriteFile(pipe, some_data)
            time.sleep(1)
            count += 1

        print("finished now")
    finally:
        win32file.CloseHandle(pipe)


def pipe_client():
    print("pipe client")
    quit = False

    while not quit:
        try:
            print(f"creating file")
            handle = win32file.CreateFile(
                pipename,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            print(f"created")
            res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
            print(f"SetNamedPipeHandleState return code: {res}")
            if res == 0:
                print(f"SetNamedPipeHandleState return code: {res}")
            while True:
                resp = win32file.ReadFile(handle, 64*1024)
                print(f"message: {resp}")
        except pywintypes.error as e:
            if e.args[0] == 2:
                print("no pipe, trying again in a sec")
                time.sleep(1)
            elif e.args[0] == 109:
                print("broken pipe, bye bye")
                quit = True
        except Exception as e:
            print(e)

def pipe_read():
    f = open(pipename,"r")
    msg = f.read()
    # AHK's write function seems to add two strange extra chars to the message
    # at the start, and adds an extra space after every other letter.
    # But python server doesn't do this.
    # msg = msg[2:]
    print(msg)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("need s or c as argument")
    elif sys.argv[1] == "s":
        pipe_server()
    elif sys.argv[1] == "c":
        pipe_client()
    elif sys.argv[1] == "r":
        pipe_read()
    else:
        print(f"no can do: {sys.argv[1]}")
