#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#warn
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#KeyHistory 0
; #persistent
#include %A_ScriptDir%\pipes.ahk

round_trip_msg(msg, pipename="test_pipe"){
   ; writePipe will block until something reads pipe.
   run, autohotkey writePipeAsync.ahk %msg% %pipename%,,,
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
   formattime, stime,,HHmmss
   n = 100
   loop %n%{
      msg=test_%A_Index%
      result := round_trip_msg(msg)
      if(result != msg){
         return false
      }
   }
   formattime, etime,,HHmmss
   t := etime - stime
   av := t/n
   msgbox tested %n% messages in %t% seconds, averaging %av% seconds per message.
   return true
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

formattime, starttime,,HHmmss
run_tests()
formattime, endtime,,HHmmss
; msgbox % "Tests took " endtime - starttime " seconds"
exitapp
