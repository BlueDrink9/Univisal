#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
; #NoTrayIcon
#KeyHistory 0
; Prevent it from triggering itself.
#inputlevel 1
#include %A_ScriptDir%\runGetOutput.ahk
global srcDir
srcDir=%A_ScriptDir%\..\..\src

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
    run python %srcDir%\univisal.py autohotkey,, hide, PID
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

univiResultFromKey(key){
    writePipe(key)
    result := readPipe()
    ; msgbox, %result%
    if (result != "nop"){
        send %result%
    }
}

toggleUnivisal(){
    if (univisalRunning()) {
        ; process, Close, %univisalPID%
        exitFunc()
    } else {
        runUnivisal()
    }
}


readPipe(){
    pipe_name := "\\.\pipe\univisal.out.fifo"
    While !DllCall("WaitNamedPipe", "Str", pipe_name, "UInt", 0xffffffff){
    ; Hoping that it should connect right away, and won't need this sleep.
        Sleep, 50
    }
    ; Assume only one line, so return after first.
    Loop, read, %pipe_name%
    {
        result := A_LoopReadLine
        ; len := strlen(result)
        ; tooltip,%len%
        if strlen(result) != 0 {
            return result
        }
    }
}


; 3 = duplex.
CreateNamedPipe(Name, OpenMode=3, PipeMode=0, MaxInstances=255){
   global ptr
   ; https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createnamedpipea
   return DllCall("CreateNamedPipe", "str", Name, "uint", OpenMode, "uint", PipeMode, "uint", MaxInstances, "uint", 0, "uint", 0, "uint", 0, ptr, 0, ptr)
}

writePipe(msg){
   ptr := A_PtrSize ? "Ptr" : "UInt"
   char_size := A_IsUnicode ? 2 : 1
   pipe_name := "\\.\pipe\univisal.in.fifo"

   pipe := CreateNamedPipe(pipe_name, 2)
   If pipe = -1
       {
       MsgBox CreateNamedPipe failed.
       ExitApp
       }
   DllCall("ConnectNamedPipe", ptr, pipe, ptr, 0)

   ; Standard AHK needs a UTF-8 BOM to work via pipe.  If we're running on
   ; Unicode AHK_L, 'msg' contains a UTF-16 string so add that BOM instead:
   ; AutoHotkey reads the first 3 bytes to check for the UTF-8 BOM "ï»¿". If it is
   ; NOT present, AutoHotkey then attempts to "rewind", thus breaking the pipe.
   msg := (A_IsUnicode ? chr(0xfeff) : chr(239) chr(187) chr(191)) . msg
   ; MsgBox % "Pipemessage is "msg
   ; https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-writefile
   If !DllCall("WriteFile", ptr, pipe, "str", msg, "uint", (StrLen(msg))*char_size, "uint*", 0, ptr, 0){
       MsgBox WriteFile failed: %ErrorLevel%/%A_LastError%
   }
   DllCall("CloseHandle", ptr, pipe)
}

F12::toggleUnivisal()
F11::exitapp
#include %A_ScriptDir%/bindings.ahk
