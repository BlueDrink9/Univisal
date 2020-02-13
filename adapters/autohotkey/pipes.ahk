readPipe(name="univisal.out.fifo"){
    pipe_name := "\\.\pipe\"name
    While !WaitForPipeConnection(pipe_name){
    ; Hoping that it should connect right away, and won't need this sleep.
        Sleep, 10
    }
    ; Assume only one line in the pipe, so return the first one.
    Loop, read, %pipe_name%
    {
        result := A_LoopReadLine
        ; len := strlen(result)
        ; tooltip,%len%
        if strlen(result) != 0 {
            return result
        }else{
            return ""
        }
    }
}

WaitForPipeConnection(pipe_name){
    return DllCall("WaitNamedPipe", "Str", pipe_name, "UInt", 0xffffffff)
}

; 3 = duplex.
CreateNamedPipe(Name, OpenMode=3, PipeMode=0, MaxInstances=255){
   global ptr
   ; https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createnamedpipea
   return DllCall("CreateNamedPipe", "str", Name, "uint", OpenMode, "uint", PipeMode, "uint", MaxInstances, "uint", 0, "uint", 0, "uint", 0, ptr, 0, ptr)
}

writePipe(msg, name="univisal.in.fifo"){
   ptr := A_PtrSize ? "Ptr" : "UInt"
   char_size := A_IsUnicode ? 2 : 1
   pipe_name := "\\.\pipe\"name

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
   msg := addBOM(msg)
   ; MsgBox % "Pipemessage is "msg
   ; https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-writefile
   If !DllCall("WriteFile", ptr, pipe, "str", msg, "uint", (StrLen(msg))*char_size, "uint*", 0, ptr, 0){
       MsgBox WriteFile failed: %ErrorLevel%/%A_LastError%
   }
   DllCall("CloseHandle", ptr, pipe)
}

addBOM(msg){
    return (A_IsUnicode ? chr(0xfeff) : chr(239) chr(187) chr(191)) . msg
}
