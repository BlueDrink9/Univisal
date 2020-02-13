#!/usr/bin/env bash
# This is just a thin CLI tool to interact with univisal.py.
# Takes only a single argument.
usage="Usage: univi.sh [key]"

TMP="${TMP:-/tmp}"

univi(){
  if [ "$#" -ne 1 ]; then
    echo "$usage"
    exit 1
  fi
  msg="$1"

  if [ ! -p "$TMP/univisal.in.fifo" ]; then
    errmsg="ERROR: No msg pipe found. Returning '$msg'"
    logMsg "$errmsg"
    printf "${msg}"
    return
  fi

  sendMsg "$msg"
  result="$(readMsg)"
  if [ ! "${result}" == "nop" ]; then
    printf "${result}"
  fi
}

sendMsg(){
  msg="$1"
  printf "${msg}" > "$TMP/univisal.in.fifo"
}
readMsg(){
  cat "$TMP/univisal.out.fifo"
}

logMsg(){
  errmsg="$1"
  # Logging by default at ERROR level. Currently unchangable
  printf "$errmsg" >> "$TMP/univisal_logs/error.log"
  printf "$errmsg" >> "$TMP/univisal_logs/debug.log"
  printf "$errmsg" >> "$TMP/univisal_logs/info.log"
}

univi "$@"
