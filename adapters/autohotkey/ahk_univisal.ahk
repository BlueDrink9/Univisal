#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
; #NoTrayIcon
#SingleInstance force
#KeyHistory 0
#include %A_ScriptDir%\pipes.ahk
#include %A_ScriptDir%\StdoutToVar.ahk
; Prevent it from triggering itself.
#inputlevel 1
global srcDir
srcDir=%A_ScriptDir%\..\..\src
#include %A_ScriptDir%\WSLSettings.ahk
univisalWSLCmd=python3 %univisalWSLPath%/src/univisal/univisal.py autohotkey

; The main function, called by every keypress.
univiResultFromKey(key){
    global useWSL
    global univisalWSLPath
    global WSLCmd

    ; Set threads to uninterruptable.
    Thread, Interrupt, -1
    if (useWSL == 1) {
        cmd=%WSLCmd% -c "%univisalWSLPath%/src/univi.sh '%key%'"  ; literal "
        result:=StdoutToVar_CreateProcess(cmd)
        send %result%
        return
    } else {
        result := getMessageResult(key)
        if (result != "nop"){
            send %result%
        }
    }
}

getMessageResult(key){
    writePipe(key)
    result := readPipe()
    return result
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

toggleUnivisal(){
    if (univisalRunning()) {
        ; process, Close, %univisalPID%
        exitFunc()
    } else {
        runUnivisal()
        sleep, 100
        if (!univisalRunning()){
            msgbox univisal failed to load. Exiting.
            exitapp
        }
    }
}

runUnivisal(){
    global useWSL
    global univisalWSLCmd
    if (useWSL == 1) {
        PID:=WSLRun(univisalWSLCmd)
    } else {
        run cmd /c python.exe -m univisal autohotkey, %srcDir%, hide, PID
    }
    setUnivisalPID(PID)
    ; msgbox running univisal with pid %PID%
    univisalPID := getUnivisalPID()
    ; Univisal should get high priority if possible, because it affects input
    ; latency.
    Process, Priority, %univisalPID%, H
}

exitFunc(){
    global useWSL
    global univisalWSLCmd
    univisalPID := getUnivisalPID()
    ; process, Close, %univisalPID%
    ; /T kills child processes, which univisal is.
    run cmd /c taskkill /pid %univisalPID% /T /F,, hide
    if (useWSL == 1) {
        cmd=pkill -9 -f '%univisalWSLCmd%'
        WSLRun(cmd)
    }
}
OnExit("exitFunc")

WSLRun(cmd){
    global WSLCmd
    run %WSLCmd% -c %cmd%,, hide, pid
    return pid
}

univisalRunning(){
    return pidExists(getUnivisalPID())
}

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

F12::toggleUnivisal()
F11::exitapp
#If univisalRunning()
#include %A_ScriptDir%/bindings.ahk
