# Univisal
Planning universal vi emulation that works across windows, OSX and linux, focusing on linux and portability.

This readme is currently just an ideas dump. Feel free to open issues with suggestions.

# Plan

## Sending and receiving keys/OS interaction handled by separate programs

#### Separate map of os-specific key combos for text actions

eg `ahk` (Windows), `sxhkd` (Linux), `hammerspoon` or `shkd` (OSX).

Keys sent to program. Program tells what keys to send out the other end. Maybe have adapter that takes command like "goEndOfLine" and sends appropriate keys. This could be a simple .json that maps the command to the necessary key strokes for an OS.

###### implemtenation ideas

* Keybind program: map every key such that it calls univisal like `univi handleKey('d')`, and then send the key returned (if any).
An skhd example: `d : skhd -k "$(univi handleKey('d'))"`
I feel like this has the most promise atm, but I'd like to get a proof-of-concept on each OS first.
As part of this, could write script to generate this sort of command for every letter/key I want to handle. Maybe take input in stringformat/printf format, eg `%s : skhd -k "$(univi handleKey('%s'))", letter, letter`.
* Write script for program that contains calls for current mode
* Call keybinding program from univisal (won't work with AHK, since it doesn't have an interface to run a single send from a command).

###### Main script takes window info, and keys

Does vi logic, maintains mode/stated, handles graphical interfcae

###### Command mode

UI box that pops up. Esc or return to exit.


###### Interface

UI box

Mode

Allow click to disable

## Server/daemon running in background to listen for responses?

## Language for main logic 

Needs to be universal/easily ported.

#### c/c++

Use gtk for gui

* Fast (! need responsiveness !)
* The norm for such programs (eg sxhkd)

* Trickier to code in/learn/maintain (lots of people know python, easy to pick up and learn)
* Needs to be compiled
* Servers/daemon programs may be trickier? (While loop listening? Check out bspwm for easy example - `bspc [cmd]`.
* Way harder to multi-thread

#### Python

Tk for gui?

* Easy to learn and pick up
* Widely available, easily installed
* Can just drop in script and run
* Plugins would be trivial to implement (can source at runtime, unlike compiled langs).
* Relatively simple to multi-thread and do complex logic and data storage with
* [Potentially can do OS-independent keypress simulation](https://rosettacode.org/wiki/Simulate_input/Keyboard#Python)

#### Rust

Is this just trendy or is it a viable replacement for c in this case? Incl. MS Windows?

## Feature list

Key to enable/disable for a given window/all over system (make this an option).

Alternatively, always active but single hotkey always enters cmd mode? I don't prefer this option, but maybe this can apply for whitelisted apps.

White/black list for always/never enable. Title matching, optionally with regex?


## Misc

[This has notes at the bottom about what emulators often miss](https://reversed.top/2016-08-13/big-list-of-vim-like-software/)
