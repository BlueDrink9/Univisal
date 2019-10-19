#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#NoTrayIcon
#KeyHistory 0

; pipename:="univisal.in.fifo"
WinUAE(command, pipename) {
    if A_IsUnicode
        command := Chr(0xFEFF) command ; UTF-16 BOM
    VarSetCapacity(result, 4096, 0)
    if !DllCall("CallNamedPipe", "str", "\\.\pipe\univisal.in.fifo"
        , "str", command, "int", (StrLen(command)+1)*(A_IsUnicode?2:1)
        , "str", result, "int", 4096
        , "uint*", bytesRead, "uint", 1){

        throw Exception("CallNamedPipe failed with error " A_LastError)
    }
    return RegExReplace(result, "\R$")
}
