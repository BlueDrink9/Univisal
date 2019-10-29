#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
; #NoTrayIcon
#KeyHistory 0
; Prevent it from triggering itself.
#inputlevel 1
#include %A_ScriptDir%\runGetOutput.ahk
global srcDir
srcDir=%A_ScriptDir%\..\src

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
    run python3 %srcDir%\univisal.py,, hide, PID
    setUnivisalPID(PID)
    univisalPID := getUnivisalPID()
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
    if (exists == 0){
        return False
    } else {
        return True
    }
}

univisalRunning(){
    return pidExists(getUnivisalPID())
}

readPipe(){
    pipe_name := "\\.\pipe\univisal.out.fifo"
    While !DllCall("WaitNamedPipe", "Str", pipe_name, "UInt", 0xffffffff){
    ; Hoping that it should connect right away, and won't need this sleep.
        Sleep, 50
    }
    ; Assume only one line, so return after first.
    Loop, read, %pipe_name%{
        return %A_LoopReadLine%
    }
}

univiResultFromKey(key){
; result := StdOutToVar("python3 " . srcDir . "\univi.py " . key)
    result : = readPipe()
    send %result%
}

toggleUnivisal(){
    if (univisalRunning()) {
        ; process, Close, %univisalPID%
        exitFunc()
    } else {
        runUnivisal()
    }
}

F12::toggleUnivisal()
F11::exitapp
#include %A_ScriptDir%/bindings.ahk
