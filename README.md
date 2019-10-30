# Univisal

Universal vi emulation that works across windows, OSX and linux/X, focusing on linux and portability.

## Concept

A vi emulator that doesn't handle key input, leaving it free to focus on the hard work of emulating vi using common system shortcuts.

Key input is handled by some other program, with an adapter written to call `univisal` and emit the responded keys.

Since [adapters](#adapters) are written for many OSes, this makes `Univisal` fairly portable.

## Installation

### Dependencies

The following is a list of python modules (usually installable through `pip`).
* `enum`
* (if on windows) `pywin32`

#### windows pipes

wpipe.py fails with error opening pipe.

serverclient server will write fine to ahk reader. univisal > ahk.
ahk write can be read with just a plain file.read operation, but this adds odd chars...
ahk write adds them if using unicode ahk. IDK why.
It also pads everything with spaces, so we want to prevent that.

### Adapters

This step of installation differs based on what adapter you want to use (see [Adapters](#adapters) for currently known options).

#### Autokey (X)

1. Start univisal.py. Do this first, otherwise your keyboard will stop working.
2. Add the adapter as a folder in Autokey. It should pick up all the hotkeys.


## Adapters

An adapter consists of config files for keybinding programs that call `univisal` some how (through an interface `univi`), and a `.json` that maps basic `univisal` movement and key commands with the string the keybinding program uses to represent those keys.
The mappings json also takes into account OS-specific shortcuts.

Generating new adapters is made simpler with `generate_adapter_bindings.py`, which can create config files with entries for each key.

* [Autohotkey](https://www.autohotkey.com) (Windows) : Needs updating for pipe system.
* [Autokey](github.com/autokey/autokey) (Xorg) : A little tricky to set up, and if univisal crashes (which it hasn't so far...) then any keys the adapter handles will stop working.
* [skhd](https://github.com/koekeishiya/skhd) (OSX) : Not written.
* [hammerspoon](https://www.hammerspoon.org/) (OSX) : Not written.
* sxhkd (Xorg) : Doesn't work. Adapter is written, but uses `xdotool` to send input, which is then recursively picked up by `sxhkd`.

## Univisal is WIP, currently using a Python and FIFO-pipe proof-of-concept

Python initial proof of concept using sockets gives unusable typing speeds.

Used pipes and the speed with python seems fine. Depends entirely on how fast the key is sent though. It may be best to just write to the pipe from ahk.

Pipes are very fast, with only a few ms of latency. Reading the key can add many more, however.

Detailed benchmarks are yet to be done.

Using autokey on Xorg seems to be working fine, at reasonable latencies - not hugely noticeable.


# Plan

## Sending and receiving keys/OS interaction handled by separate programs

#### Separate map of os-specific key combos for text actions

eg `ahk` (Windows), `sxhkd` (Linux/X input) + `xdotool` (Linux/X output), `hammerspoon` or `shkd` (OSX).

Keys sent to program. Program tells what keys to send out the other end. Maybe have adapter that takes command like "goEndOfLine" and sends appropriate keys. This could be a simple .json that maps the command to the necessary key strokes for an OS.

###### implementation ideas

* Keybind program: map every key such that it calls univisal like `univi handleKey('d')`, and then send the key returned (if any).
An skhd example: `d : skhd -k "$(univi handleKey('d'))"`  
An sxhkd+xdotool example: `d \n xdotool key $(univi handleKey('d'))`

I feel like this has the most promise atm, but I'd like to get a proof-of-concept on each OS first.

Would still need a way to map desired output to a key/command in format the OS tool can use, which brings back the json.
But if using [autopilot-rs](https://github.com/autopilot-rs/autopilot-rs), only need to handle OS-specific behaviour, not tool-specific. (Ie rust or python).

As part of this, could write script to generate this sort of command for every letter/key I want to handle. Maybe take input in stringformat/printf format, eg `%s : skhd -k "$(univi handleKey('%s'))", letter, letter`.

* Write script for program that contains calls for current mode
* Call keybinding program from univisal (won't work with AHK, since it doesn't have an interface to run a single send from a command).
* Spin off a subprocess/backgrounded 'server' univisal, and have a function 'univi' that writes to its stdin and reads its stdout. Might only work for root though... May have to create own pipe.
https://serverfault.com/questions/178457/can-i-send-some-text-to-the-stdin-of-an-active-process-running-in-a-screen-sessi 
https://wiki.wireshark.org/CaptureSetup/Pipes#Way_3:_Python_on_Windows
https://stackoverflow.com/questions/48542644/python-and-windows-named-pipes

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
* [Potentially can do OS-independent keypress simulation](https://rosettacode.org/wiki/Simulate_input/Keyboard#Python), which would be especially convinient for linux/X.

#### Rust

Is this just trendy or is it a viable replacement for c in this case? Incl. MS Windows?

* [Potentially can do OS-independent keypress simulation](https://rosettacode.org/wiki/Simulate_input/Keyboard#Rust)

## Feature list / roadmap

Key to enable/disable for a given window/all over system (make this an option).

Alternatively, always active but single hotkey always enters cmd mode? I don't prefer this option, but maybe this can apply for whitelisted apps.

White/black list for always/never enable. Title matching, optionally with regex?

For speed, potentially have an option where the key grab software passes key straight back if it is insert mode, only enables maps in normal mode. Would mean insert mappings aren't possible, but not everyone uses.
Have a function/command callable from univi that returns current mode?

Remember insert mode entries. Parse for imaps, and allow `.` repeats.

Benchmark latency using https://github.com/pavelfatin/typometer

Tests to compare text change parity with vim.

Way to edit the cursor shape of the system, or otherwise have a visual indication close to the text about mode.

## Hacking together motions and operators from OS shortcuts

`^`: Possible home, then ctrl+right+left, to go BoL->Eo first word -> Bo first word.

## Benchmarking

In one terminal: `f(){ echo "h" > /tmp/univisal.in.fifo; cat /tmp/univisal.out.fifo ; }`
In another: `while true; do cat /tmp/univisal.in.fifo > /tmp/uni; done`
In first term again: `time f`

> real	0m0.004s
> user	0m0.004s
> sys	0m0.000s

This remains broadly the same when running `univisal.py` in the second terminal instead, version at this commit.

## 

## Misc

Note: in vim, counts before an operator multiply with the count after the operator.

In vim, operators leave the cursor at the left of the text operated on.

Read through [normal.c](https://github.com/neovim/neovim/blob/master/src/nvim/normal.c) to understand how vim's architecture handles normal mode etc.

Also skim [ops.c](https://github.com/neovim/neovim/blob/master/src/nvim/ops.c)

[This has notes at the bottom about what emulators often miss](https://reversed.top/2016-08-13/big-list-of-vim-like-software/)

[Article about latency measurements](https://pavelfatin.com/typing-with-pleasure/)

[Use typometer to benchmark/measure latency](https://pavelfatin.com/typometer/)

# Alternatives/similar projects

## Windows

I recommend [vim_ahk](https://github.com/rcmdnk/vim_ahk). It is relatively feature-full, and actively maintained.
It's currently far better than Univisal. Probably faster, too.

It is, however, limited by its ahk model. Adding imaps is an absolute pain, and is something I want Univisal to handle much better.

## OSX

A [handful](https://www.reddit.com/r/vim/comments/56twvs/modal_keybindings_everywhere_with_hammerspoon_mac/) of [Hammerspoon](https://github.com/wingillis/hammerspoon-vim-bindings) vim spoons exist. None are phenominal, most are fine.

## Xorg

None that I know of, which was the main motivation for writing this.

I just decided that, if I was going to put time into another emulator, I wanted it to be a good one and therefore I wanted to use it on any OS.
Hence, Univisal was born.
