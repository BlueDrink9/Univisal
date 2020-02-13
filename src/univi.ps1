# This is just a thin CLI tool to interact with univisal.py.
# Usage: univi.ps1 [key]
# Takes only a single argument.

function writePipe($pipename, $msg){
    $pipe = new-object System.IO.Pipes.NamedPipeServerStream "$pipename",'Out'
    $pipe.WaitForConnection()
    $sw = new-object System.IO.StreamWriter $pipe
    $sw.AutoFlush = $true
    $sw.WriteLine("$msg")
    $sw.Dispose()
    $pipe.Dispose()
}

function readPipe($pipename){
    $pipe = new-object System.IO.Pipes.NamedPipeClientStream '.',"$pipename",'In'
    $pipe.Connect()
    $sr = new-object System.IO.StreamReader $pipe
    while (($data = $sr.ReadLine()) -ne $null) { "$data" }
    $sr.Dispose()
    $pipe.Dispose()
}
writePipe "univisal.in.fifo" "l"
readPipe("univisal.out.fifo")
