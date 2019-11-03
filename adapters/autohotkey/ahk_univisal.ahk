#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
; #NoTrayIcon
#KeyHistory 0
#include %A_ScriptDir%\pipes.ahk
; Prevent it from triggering itself.
#inputlevel 1
global srcDir
srcDir=%A_ScriptDir%\..\..\src

; The main function, called by every keypress.
univiResultFromKey(key){
    writePipe(key)
    result := readPipe()
    ; msgbox, %result%
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
    }
}

F12::toggleUnivisal()
F11::exitapp
#include %A_ScriptDir%/bindings.ahk
