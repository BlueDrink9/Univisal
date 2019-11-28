#!/usr/bin/env bash

SCRIPTDIR_CMD='eval echo $(cd $( dirname "${BASH_SOURCE[0]}" ) && pwd)'
SCRIPTDIR="$($SCRIPTDIR_CMD)"
UNIVISAL_DIR="$(realpath "${SCRIPTDIR}/../..")"
# Source univi() with blank arg to skip inital run.
. "${UNIVISAL_DIR}/src/univi.sh" ""
# This was just the func name used in bindings.sxhkd.
# Could be changed if wanted, to just call univi directly.
univi_handleKey(){ univi "${1}"; };

export UNIVISAL_DIR
export -f univi_handleKey

# Possible TODO: Also source the main sxhkd so user bindings don't get overridden?
sxhkd -m -1 -c "$SCRIPTDIR/bindings.sxhkd" "$SCRIPTDIR/bindings_extra.sxhkd"  \
  # > $HOME/.logs/univisal_sxhkd.log 2> $HOME/.logs/univisal_sxhkd.err &
