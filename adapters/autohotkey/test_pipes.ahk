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
#include %A_ScriptDir%\instance.ahk
If Instance("","-")   ; this is in the autoexecute section to initialize
 Return               ; and to redirect when a special instance is started

round_trip_msg(msg, pipename="test_pipe"){
   ; writePipe will block until something reads pipe.
   ; Need to pass params in 2nd arg.
   pid := Instance("-writethread", msg " " pipename)
   ; readPipe will block until something is written to pipe.
   result := readPipe(pipename)
   return result
}

test_single_char(){
   msg=t
   result := round_trip_msg(msg)
   if(result != msg){
      return false
   }else{
      return true
   }
}

test_multi_char(){
   msg=test_message
   result := round_trip_msg(msg)
   if(result != msg){
      return false
   }else{
      return true
   }
}

test_multi_msg(){
   loop, 10{
      msg=test %A_Index%
      result := round_trip_msg(msg)
      if(result != msg){
         return false
      }else{
         return true
      }
      sleep, 100
   }
}

run_tests(){
   failed := false
   tests:=["test_single_char"
   , "test_multi_char"
   , "test_multi_msg"]
   results:=[]
   Loop % tests.Length(){
      test := tests[A_Index]
      ; Run this test function
      results[A_Index] := %test%()
   }
   Loop % results.Length(){
      if (!results[A_Index]){
         test := tests[A_Index]
         failed := true
         msgbox Failed test %test%
      }
   }
   if (!failed){
      msgbox All passed!
   }
}

run_tests()
exitapp

-writethread:
   ; msg can't contain spaces or this breaks.
   writemsg=%2%
   pipename=%3%
   Menu Tray, Tip, writer
; msgbox %msg%
; msgbox %pipename%
   writePipe(writemsg, pipename)
   exitapp
return
