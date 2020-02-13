# This is just a thin CLI tool to interact with univisal.py.
# Usage: univi.ps1 [key]
# Takes only a single argument.
$usage="Usage: univi.ps1 [key]"

# Note: Powershell scripts are probably too slow to startup to be useful here.
# VBS should be better if I can get pipes working.

if ($args.count -ne 1){
    echo "$usage"
    exit 1
}
$msg = $args[0]

function univi($msg){
    ## Can we check that the pipe exists? Not sure. XXX
    # if !pipeExists(){
    #     errmsg="ERROR: No msg pipe found. Returning '$msg'"
    #     logMsg "$errmsg"
    #     printf "${msg}"
    #     return
    # }

    sendMsg "$msg"
    $result="$(readMsg)"
    if ("$result" -ne "nop"){
        echom "$result"
    } else {
        echom ""
    }
}

function sendMsg($msg){
    $pipename="univisal.in.fifo"
    $pipe = new-object System.IO.Pipes.NamedPipeServerStream "$pipename",'Out'
    $pipe.WaitForConnection()
    $sw = new-object System.IO.StreamWriter $pipe
    $sw.AutoFlush = $true
    $sw.WriteLine("$msg")
    $sw.Dispose()
    $pipe.Dispose()
}

function readMsg(){
    $pipename="univisal.out.fifo"
    $pipe = new-object System.IO.Pipes.NamedPipeClientStream '.',"$pipename",'In'
    $pipe.Connect()
    $sr = new-object System.IO.StreamReader $pipe
    while (($data = $sr.ReadLine()) -ne $null) { "$data" }
    $sr.Dispose()
    $pipe.Dispose()
}

function echom($text){
    write-output($text)
}

univi $msg
