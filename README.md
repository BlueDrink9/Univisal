# Univisal

Universal vi emulation that works across windows, OSX and linux/X, focusing on linux and portability.

## Concept

A vi emulator that doesn't handle key input, leaving it free to focus on the hard work of emulating vi using common system shortcuts.

Key input is handled by some other program, with an adapter written to call `univisal` and emit the responded keys.

Since [adapters](#adapters) are written for many OSes, this makes `Univisal` fairly portable.

## Configuration

Configuration is done by `config.json` in `$XDG_CONFIG_HOME/univisal/` or `~/.config/univisal/`.

If this file is not present, defaults will be created.

| option | description | default | Valid values |
|--------|--------|---------|---------|
| load_config | A list of paths to alternative `json`s to load after the main config. `~` is expanded. | [] | string |
| log_level | Level of logs to output to stderr and the log files | "warning" | "debug", "info", "warning", "error", "critical" |
| swallow_unused_normal_keys | Whether unused keys in normal mode should send the base key (false) or send nothing (true) | "false" | "true", "false" |
| imaps | Map of key:value pairs to expand in insert mode. | {} |  |
| nmaps |  Map of key:value pairs to expand in normal mode. | {} | Left hand side must be a single keypress |
| vmaps, cmaps | Map of key:value pairs to expand in visual or command modes. | {} | None, currently unimplimented. |

Due to technical limitations (can't undo normal commands) only single keypresses are permitted for normal map left hand sides.

## Installation

### Dependencies

The following is a list of python modules (usually installable through `pip`).
* `enum`
* (if on windows) `pywin32`

#### windows pipes

Currently is working, but very slow. Look at optimising opening and closing of pipes.
Also univisal occasionally gets stuck waiting for AHK to read pipe. Does AHK wait for something to be readable? No!

### Adapters

This step of installation differs based on what adapter you want to use (see [Adapters](#adapters) for currently known options).

#### Autokey (X)

1. Start univisal.py. Do this first, otherwise your keyboard will stop working.
2. Add the adapter as a folder in Autokey. It should pick up all the hotkeys.


## Adapters

An adapter consists of config files for keybinding programs that call `univisal` some how (through an interface `univi`), and a `.json` that maps basic `univisal` movement and key commands with the string the keybinding program uses to represent those keys.
The mappings json also takes into account OS-specific shortcuts.

#### Windows

###### [Autohotkey](https://www.autohotkey.com)

Currently poor latency because of how windows handles named pipes. (However, this seems to be more a problem with how AHK interacts with them than the pipe speeds themselves, which from python tests are fast enough).

There is also an option to use Linux FIFO pipes via WSL, but this currently has even worse latencies. This suggests it isn't the windows pipes that were causing the problems, unless the `wsl -c` use is the bottleneck.

To use WSL, in the adapters folder, create a file called WSLSettings.ahk, and set 3 options:

* `useWSL` 1 or 0 depending on whether you want to use WSL paths.
* `univisalWSLPath` to the path of this repo from within WSL (eg `/bin/univisal`)
* `WSLCmd` to the cmd to run WSL (eg `bash.exe` or `ubuntu.exe`)

#### Linux/Xorg

###### [Autokey](github.com/autokey/autokey)

A little tricky to set up, and if univisal crashes (which it hasn't so far...) then any keys the adapter handles will stop working.

Requires the `develop` branch of autokey.

Add the adapter folder in autokey, and set things up to run `bindings.py` on startup. `autokey-run -s bindings`, where "bindings" is the script description in autokey.

Currently there's a bug where each key is inputted twice. Instant workaround: as soon as bindings is run, use your key to disable autokey expansion, then re-enable it.

###### sxhkd

Doesn't work. Adapter is written, but uses `xdotool` to send input, which is then recursively picked up by `sxhkd`.

If this can be fixed, this adapter should work.

#### OSX

###### [skhd](https://github.com/koekeishiya/skhd)

Not written.

###### [hammerspoon](https://www.hammerspoon.org/)

Not written.


#### Generating adapters

Generating new adapters is made simpler with `generate_adapter_bindings.py`, which can create config files with entries for each key univisal needs to handle, mapped with an appropriate `mappings.json` file in the adapter directory.

Once the file is generated, additional code usually needs to be added. At minimum, some function that sends the right string to the main univisal process.

On Windows, adapters should handle a few special return cases from univisal:

* `<requestSelectedText>`
* ...

On unix, `src/univi.sh` handles these cases for you. Adapters should simply call `src/univi.sh` with the input to be sent as an argument, and capture the `stdout` as the output. For example `output="$(src/univi.sh '<esc>')"`.

Usage: `generate_adapter_bindings.py adapter 'string'`

Args:

* `adapter`: name generated bindings will write as. Should be the name of a folder in `adapters` containing a valid `mappings.json`.
* `string` : a printf-formatted string. It is the command to generate for the adapter, with %s in two places: Binding and send position.

Examples:

* `autohotkey`: `%s::univiResultFromKey(\"%s\")`
    * creates `d::univiResultFromKey("d")` 
* `sxhkd`: `%s\n\txdotool key $(univi_handleKey %s)`
    * creates
    ```
    d
        xdotool key $(univi_handleKey 'd')
    ```
* `autokey < 0.96`: `create_hotkey(folder, \"desc\", [], \"%s\", \"<script name=univi args=%s>\", temporary=True)`
    * creates `create_hotkey("univisal", "desc", [], "d", "d")`
* `autokey > 0.96`: `create_phrase(folder, \"desc\", \"<script name=univi args=%s>\", hotkey=\"%s\", temporary=True)`
    * creates `create_phrase(folder, "desc", "<script name=univi args=d>", hotkey="d", temporary=True)`
* A much easier version declares a wrapper func in the binding file that calls the above functions. `bind(\"%s\", \"%s\")`

#### mappings.json

This is a simple json with values as the representation of any special keys for the adapter, eg `{escape}` for autohotkey. Keys are the string univisal uses for that key, as found in the table under **Key representations**.

Any key without an adapter map will be send as the input string.

## Testing

Download [`pytest`](https://docs.pytest.org/en/latest/getting-started.html) using `pip install pytest`.

Run from the root repo dir using `python -m pytest` (or just `pytest` seems to work, but [may have issues with which directory it is run by)](https://docs.pytest.org/en/latest/pythonpath.html#pytest-vs-python-m-pytest).

## Key representations (documentation under construction).

Univisal tries to use the same representation as vim keycodes in `:h intro`, for example in mappings (`inoremap jj <Esc>`). 
This means they can be inserted using `^V`.
Exceptions are keys that send their non-whitespace text representation when pressed, like `|` (`<Bar>`).

The representations are also only lowercase.

Modifier keys are their standard name, since vim normally only maps them with another key, e.g. <shift>.

Any other keys are listed here.

| key | Univisal representation |
|-----|-------------------------|
| capslock | `"<capslock>"` |
| enter/return | `"<enter>"` |
| ctrl | `"<ctrl>"` |
| shift | `"<shift>"` |
| alt | `"<alt>"` |
| super/winkey | `"<super>"` |
<!-- | spacebar | "space" | -->

## Special 'keys'

These are strings to send as keys or to map that have special meaning.

| key | Univisal representation |
|-----|-------------------------|
| `"<multikey_join_char>"` | String to tell adapter to send multiple keys from one response, each key specified by this character |


## Univisal is WIP, currently using a Python and FIFO-pipe proof-of-concept

Python initial proof of concept using sockets gives unusable typing speeds.

Used pipes and the speed with python seems fine. Depends entirely on how fast the key is sent though. It may be best to just write to the pipe from ahk.

Pipes are very fast, with only a few ms of latency. Reading the key can add many more, however.

Detailed benchmarks are yet to be done.

Using autokey on Xorg seems to be working fine, at reasonable latencies - not hugely noticeable.

On windows, python pipe latency is fine (<0.4 ms for 30 messages) according to `test_pipes_windows.py`. However, when using ahk, latency jumps 10-fold. AHK's pipe writing/reading methods seem to be a bottleneck.

Reading and writing in ahk for 100 messages in a loop takes 3 seconds. 
Only reading in ahk and writing in python reduce it to at most 1 second for 100 messages.
Only writing in ahk and reading in python reduce it to at most 1 second for 100 messages.


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

## Feature list / roadmap

Key to enable/disable for a given window/all over system (make this an option).

Alternatively, always active but single hotkey always enters cmd mode? I don't prefer this option, but maybe this can apply for whitelisted apps.

White/black list for always/never enable. Title matching, optionally with regex?

For speed, potentially have an option where the key grab software passes key straight back if it is insert mode, only enables maps in normal mode. Would mean insert mappings aren't possible, but not everyone uses.
Have a function/command callable from univi that returns current mode? Maybe change <nop> output for keys that enter normal mode to <normal>?
Probably adapter-dependent.
Can send the key to univisal regardless, to keep it updated of current mode, but sends key straight away if in insert mode (ie without waiting for univisal response.) (Although for the pipes it will still have to read and discard the output.)

Remember insert mode entries. Parse for imaps, and allow `.` repeats.

Benchmark latency using https://github.com/pavelfatin/typometer

[x] Tests to compare text change parity with vim.

Way to edit the cursor shape of the system, or otherwise have a visual indication close to the text about mode.

setting: allow specifying the binary for adapters (so they don't have to be on the path).

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

[Notes and suggestions from a kind redditor about the processing model](https://www.reddit.com/r/vim/comments/el2rcl/describe_the_basic_normal_mode_algorithm/)

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


# TODO

VisualLine, VisualChar modes

Replace mode?

Record normal commands, insert commands for dot redo?
