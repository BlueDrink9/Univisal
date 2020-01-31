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

## Normal mode algorithm

Based of [this post reply](https://www.reddit.com/r/vim/comments/el2rcl/describe_the_basic_normal_mode_algorithm/fdgo9ad)

make a data structure that will contain count and information about range for a command to operate on (empty range and no count initially). - This in model.

Flag keys for operators as things that accept motion/selection.
handleKey/normal.py is list of keys. Keys have flags and hander functions.
Include gg in this list?

Have additional list of selectors/motions (e.g., "j", "gg", "iw") along with handlers.

built a list of builtin mappings with entries containing: key combination (e.g., "G" and "gg"), flags (e.g., "accepts selector"), handler (function that accepts data structure, can be read-only)

built a list of selectors with entries containing: key combination (e.g., "j", "gg", "iw"), handler (function that accepts the same, but this time writable data structure)

Make main key handling function (KHF). It should:

Accept current input buffer and as a result inform its caller about whether input was processed or not (nop/requestReturn?). If not finished, keep storing keys! If not finished, will not be ambiguous.

Extract count from the beginning of input string if there is a count

Look for the **longest match among mappings**

If there are **no matches**, discard the input, it's wrong (more Vim-like behaviour is to discard one character at a time and try to parse input again, you can do it this way)

If there is *more than one match*, return keeping input (need more keys to disambiguate it)

Otherwise, we have a match.

If it doesn't need a selector (motion or text object), invoke the handler giving it a count. Done.

If it requires a selector, you can read second count here ("2d6j" is a valid command) and multiply it with the previous one ("2d6j" == "16dj").

Now pass the count and your data structure to selector handler, whose job is to come up with the range and put it in your data structure.

Invoke mapping handler passing it range information (count shouldn't be needed here). Done.

Outside of KHF you keep a buffer to which you append user's input and invoke KHF after which you either leave the buffer untouched, clear it or drop the first character and call KHF again (per txt in parenthesis in bullet #3 above).

Check out [vim_ahk](https://github.com/rcmdnk/vim_ahk/blob/master/vim.ahk) for more implementation suggestions, esp for windows.

Motions are done in a loop if operator pending, with shift down.

In visual mode, all motions are prepended with shift down, finished with shift up.

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
