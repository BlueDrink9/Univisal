#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; Need to start write as separate instance.
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

msg=test message
pipename=test_pipe2
msgbox, before thread
pid := Instance("-writethread", pipename)
msgbox, after thread
; return
sleep, 100
msgbox, before read
result := readPipe(pipename)
msgbox, after read
if(result != msg){
   msgbox Failed
}else{
   msgbox Pass
}
exitapp

-writethread:
   pipename=%2%
   msgbox, writethread
   writePipe(msg, pipename)
   ; SetTimer,, Off
   ; exit
return
