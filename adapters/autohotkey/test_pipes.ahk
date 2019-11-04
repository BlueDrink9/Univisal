#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; Need to start writepipe as separate instance.
#SingleInstance off
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#KeyHistory 0
; #persistent
#include %A_ScriptDir%\pipes.ahk
#include %A_ScriptDir%\instance.ahk
If Instance("","-")   ; this is in the autoexecute section to initialize
 Return               ; and to redirect when a special instance is started

msg=test_message
pipename=test_pipe
; Need to pass params in 2nd arg.
pid := Instance("-writethread", msg " " pipename)
; return
; sleep, 100
result := readPipe(pipename)
if(result != msg){
   msgbox Failed
}else{
   msgbox Pass
}
exitapp

-writethread:
   ; msg can't contain spaces or this breaks.
   msg=%2%
   pipename=%3%
; msgbox %msg%
; msgbox %pipename%
   writePipe(msg, pipename)
   exitapp
return
