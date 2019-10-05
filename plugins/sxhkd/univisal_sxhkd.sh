#!/usr/bin/env bash

SCRIPTDIR_CMD='eval echo $(cd $( dirname "${BASH_SOURCE[0]}" ) && pwd)'
SCRIPTDIR="$($SCRIPTDIR_CMD)"
UNIVISAL_DIR="$(realpath "${SCRIPTDIR}/../..")"
# Source univi()
. "${UNIVISAL_DIR}/src/univi.sh"
univi_handleKey(){
  key="$1"
  univi "${key}"
  # python3 "${UNIVISAL_DIR}"/src/univi.py "${key}"
  # bash -c "\"${UNIVISAL_DIR}\"/src/univi.sh \"${key}\""
}
export UNIVISAL_DIR
export -f univi_handleKey

# Possible TODO: Also source the main sxhkd so user bindings don't get overridden?
sxhkd -m -1 -c "$SCRIPTDIR/bindings.sxhkd" "$SCRIPTDIR/bindings_extra.sxhkd"  \
  # > $HOME/.logs/univisal_sxhkd.log 2> $HOME/.logs/univisal_sxhkd.err &
