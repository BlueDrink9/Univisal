REM Windows batch file version.
REM This is just a thin CLI tool to interact with univisal.py.
REM Usage: univi.py [key]
REM Takes only a single argument.

univi(){
  if [ "$#" -ne 1 ]; then
    echo "Usage: univi.py [key]"
    exit 1
  fi

  sendKey "$1"
  result="$(readKey)"
  if [ ! "${result}" == "NOP" ]; then
    printf "${result}"
  fi
}

sendKey(){
  echo %1% >\\.\pipe\univisal_in
}
readKey(){
  type \\.\pipe\univisal_out
  rem set /p key=<\\.\pipe\univisal_out
  rem echo %key%
}

# univi "$@"
