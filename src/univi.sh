#!/usr/bin/env bash
# This is just a thin CLI tool to interact with univisal.py.
# Usage: univi.py [key]
# Takes only a single argument.

TMP="${TMP:-/tmp}"

univi(){
  if [ "$#" -ne 1 ]; then
    echo "Usage: univi.py [key]"
    exit 1
  fi

  if [ ! -p "$TMP/univisal.in.fifo" ]; then
    printf "${1}"
    errmsg="ERROR: No input pipe found. Returning $1"
    printf "$errmsg" >> "$TMP/univisal_logs/error.log"
    printf "$errmsg" >> "$TMP/univisal_logs/debug.log"
    printf "$errmsg" >> "$TMP/univisal_logs/info.log"
    return
  fi

  sendKey "$1"
  result="$(readKey)"
  if [ ! "${result}" == "nop" ]; then
    printf "${result}"
  fi
}

sendKey(){
  key="$1"
  printf "${key}" > "$TMP/univisal.in.fifo"
}
readKey(){
  cat "$TMP/univisal.out.fifo"
}

univi "$@"
