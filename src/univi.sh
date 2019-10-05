#!/usr/bin/env bash
# This is just a thin CLI tool to interact with univisal.py.
# Usage: univi.py [key]
# Takes only a single argument.

if [ "$#" -ne 1 ]; then
  echo "Usage: univi.py [key]"
  exit 1
fi

sendKey(){
  key="$1"
  printf "${key}" > /tmp/univisal.in.fifo
}
readKey(){
  cat /tmp/univisal.out.fifo
}

sendKey "$1"
result="$(readKey)"
if [ ! "${result}" == "NOP" ]; then
    printf "${result}"
fi
