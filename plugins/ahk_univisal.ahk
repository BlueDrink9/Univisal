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

run %srcDir%\univisal.py,, hide, univisalPID
global univisalPID
runUnivisal(){
    global univisalPID
    run %srcDir%\univisal.py,, hide, univisalPID
    Process, Priority, %univisalPID%, H
    msgbox, run %univisalPID%
}
exitFunc(){
    global univisalPID
    process, Close, %univisalPID%
}
OnExit("exitFunc")

univiResultFromKey(key){
    result := StdOutToVar("python3 " . srcDir . "\univi.py " . key)
    send %result%
}

toggleUnivisal(){
msgbox, toggle
    if Process, Exist, %univisalPID% {
        msgbox, exists
        ; process, Close, %univisalPID%
        exitFunc()
    } else {
        msgbox, No exist
        runUnivisal()
    }
}

F12::toggleUnivisal()
F11::exitapp
#include %A_ScriptDir%/bindings.ahk
