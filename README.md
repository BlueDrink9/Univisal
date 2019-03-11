# Univisal
Planning universal vi emulation that works across windows, OSX and linux, focusing on linux and portability.

# Plan

###### Separate map of os-specific key combos for text actions

###### Sending and recioving keys handled by separate program

eg `ahk` (Windows), `sxhkd` (Linux), `hammerspoon` or `shkd` (OSX).

Keys sent to program. Program tells what keys to send out the other end. Maybe have adapter that takes command like "goEndOfLine" and sends appropriate keys

###### Main script takes window info, and keys

Does vi logic, maintains mode/stated, handles graphical interfcae

###### Command mode

UI box that pops up. Esc or return to exit.

###### Interface

UI box

Mode

Allow click to disable
