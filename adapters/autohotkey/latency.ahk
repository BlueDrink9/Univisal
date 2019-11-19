#warn
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#NoTrayIcon
#KeyHistory 0
#inputlevel 1
#include %A_ScriptDir%\pipes.ahk

global srcDir
srcDir=%A_ScriptDir%\..\..\src

; The main function, called by every keypress.
univiResultFromKey(key){
    ; The problem here is that when using hotkeys, which spawn new threads each
    ; time, you may get a new call to write when the previous one hasn't
    ; finished.
    ; This lock aims to solve that.
    ; Need to wait for write to finish, and read to return, before writing
    ; anything else. Otherwise, AHK's main thread locks waiting for a read to
    ; happen on .in.fifo. The problem arises when a hotkey spawns another
    ; thread that requests a write, while univisal is writing to .out and
    ; waiting for a read from the original?

    ; Set threads to uninterruptable.
    Thread, Interrupt, -1
    writePipe(key)
    result := readPipe()
    if (result != "nop"){
        send %result%
    }
}

global univisalPID = 0
getUnivisalPID(){
    global univisalPID
    return univisalPID
}
setUnivisalPID(pid){
    global univisalPID
    univisalPID := pid
}

runUnivisal(){
    run python %srcDir%\univisal\univisal.py autohotkey,, hide, PID
    setUnivisalPID(PID)
    ; msgbox running univisal with pid %PID%
    univisalPID := getUnivisalPID()
    ; Univisal should get high priority if possible, because it affects input
    ; latency.
    Process, Priority, %univisalPID%, H
}
exitFunc(){
    univisalPID := getUnivisalPID()
    process, Close, %univisalPID%
}
OnExit("exitFunc")

pidExists(pid){
    Process, Exist, %pid%
    exists := ErrorLevel
    ; Verbose, but easier than trying to remember what each errorlevel means
    if (exists == 0){
        return False
    } else {
        return True
    }
}

univisalRunning(){
    return pidExists(getUnivisalPID())
}

toggleUnivisal(){
    if (univisalRunning()) {
        ; process, Close, %univisalPID%
        exitFunc()
    } else {
        runUnivisal()
        if (!univisalRunning()){
            msgbox univisal failed to load. Exiting.
            exitapp
        }
    }
}

runUnivisal()
formattime, starttime,,HHmmss
loop, 50{
    univiResultFromKey("l")
    }
formattime, endtime,,HHmmss
msgbox % endtime - starttime
toggleUnivisal()
