#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#warn
; Need to start writepipe as separate instance.
#SingleInstance off
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#KeyHistory 0
; #persistent
#include %A_ScriptDir%\pipes.ahk

a_pipe = %2%
loop, 100{
    a_msg = %a_index%
    writePipe(a_msg, a_pipe)
}
