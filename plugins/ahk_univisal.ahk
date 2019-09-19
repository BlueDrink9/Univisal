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
exitFunc(){
    process, Close, %univisalPID%
}
OnExit("exitFunc")

univiResultFromKey(key){
    result := StdOutToVar("python " . srcDir . "\univi.py " . key)
    send %result%
}
m::univiResultFromKey("m")
d::univiResultFromKey("d")
0::univiResultFromKey("d")
