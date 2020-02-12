# Univisal

Universal vi emulation that works across windows, OSX and linux/X11, focusing on linux and portability.

## Concept

A vi emulator that doesn't handle key input, leaving it free to focus on the hard work of emulating vi using common system shortcuts.

Key input is handled by some other program, with an adapter written to call `univisal` and emit the responded keys.

Since [adapters](#adapters) are written for many OSes, this makes `Univisal` fairly portable.

## Usage

Univisal can be started one of two ways:

* Run one of the adapters, which should start univisal with the correct parameters
* Manually `cd` to `univisal/src` and run `python3 -m univisal [adapter]`

## Configuration

Configuration is done by `config.json` in `$XDG_CONFIG_HOME/univisal/` or `~/.config/univisal/`.

If this file is not present, defaults will be created.

| option | description | default | Valid values |
|--------|--------|---------|---------|
| load_config | A list of paths to alternative `json`s to load after the main config. `~` is expanded. | [] | string |
| log_level | Level of logs to output to stderr and the log files | "warning" | "debug", "info", "warning", "error", "critical" |
| swallow_unused_normal_keys | Whether unused keys in normal mode should send the base key (false) or send nothing (true) | false | true, false |
| imaps | Map of key:value pairs to expand in insert mode. | {} |  |
| nmaps |  Map of key:value pairs to expand in normal mode. | {} | Left hand side must be a single keypress |
| vmaps, cmaps | Map of key:value pairs to expand in visual or command modes. | {} | None, currently unimplimented. |

Due to technical limitations (can't undo normal commands) only single keypresses are permitted for normal map left hand sides.

Log level is set to DEBUG until configuration is loaded, so you will see any log messages related to initialising univisal config.

## Installation

### Dependencies

The following is a list of python modules (usually installable through `pip`).
* `enum`
* (if on windows) `pywin32`

### Adapters

This step of installation differs based on what adapter you want to use (see [Adapters](#adapters) for currently known options).

#### X11

##### Autokey

1. `autokey-run path/to/repo/adapters/autokey_univisal/autokey_univisal.py`
2. If you are already using hotkeys this script uses in any of its modes, running this script will replace them.

#### Windows

##### Autohotkey/AHK

Run `adapters/autohotkey/univisal.ahk` using autohotkey.

#### OSX

##### skhd

TBD.

## Adapters

An adapter consists of config files for keybinding programs that call `univisal` somehow (through an interface `univi`), and a `.json` that maps basic `univisal` movement and key commands with the string the keybinding program uses to represent those keys.
The mappings json also takes into account OS-specific shortcuts.

If you want to use a keybinding system that isn't on this list, open an issue or (better yet) write one and open a PR. See [Writing adapters](docs/adapters.md) for more on adding and editing adapters.

#### Windows

###### [Autohotkey](https://www.autohotkey.com)

Currently poor latency because of how windows handles named pipes. (However, this seems to be more a problem with how AHK interacts with them than the pipe speeds themselves, which from python tests are fast enough).

There is also an option to use Linux FIFO pipes via WSL, but this currently has even worse latencies. This suggests it isn't the windows pipes that were causing the problems, unless the `wsl -c` use is the bottleneck.

To use WSL, in the adapters folder, create a file called WSLSettings.ahk, and set 3 options:

* `useWSL` 1 or 0 depending on whether you want to use WSL paths.
* `univisalWSLPath` to the path of this repo from within WSL (eg `/bin/univisal`)
* `WSLCmd` to the cmd to run WSL (eg `bash.exe` or `ubuntu.exe`)

I have a suspicion the slowness is due to reading on standard io streams from AHK. Using window messages may work better.

#### Linux/X11

###### [Autokey](github.com/autokey/autokey)

A little tricky to set up, and if univisal crashes (which it hasn't so far...) then any keys the adapter handles will stop working.

Requires the `develop` branch of autokey, or version >= `0.96`, which is unreleased at time of writing.

Currently there's a bug where each key is inputted twice. Instant workaround: as soon as bindings is run, use your key to disable autokey expansion, then re-enable it.

###### sxhkd

Doesn't work. Adapter was written, but uses `xdotool` to send input, which is then recursively picked up by `sxhkd`.

If this can be fixed, this adapter should work.

#### OSX

###### [skhd](https://github.com/koekeishiya/skhd)

Not written.

###### [hammerspoon](https://www.hammerspoon.org/)

Not written.


## Univisal is WIP, currently using a Python and FIFO-pipe proof-of-concept

Python initial proof of concept using sockets gives unusable typing speeds.

Used pipes and the speed with python seems fine. Depends entirely on how fast the key is sent though. It may be best to just write to the pipe from ahk.

Pipes are very fast, with only a few ms of latency. Reading the key can add many more, however.

Detailed benchmarks are yet to be done.

Using autokey on X11 seems to be working fine, at reasonable latencies - not hugely noticeable.

On windows, python pipe latency is fine (<0.4 ms for 30 messages) according to `test_pipes_windows.py`. However, when using ahk, latency jumps 10-fold. AHK's pipe writing/reading methods seem to be a bottleneck.

Reading and writing in ahk for 100 messages in a loop takes 3 seconds.
Only reading in ahk and writing in python reduce it to at most 1 second for 100 messages.

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

#### Unix pipe latency

In one terminal: `f(){ echo "h" > /tmp/univisal.in.fifo; cat /tmp/univisal.out.fifo ; }`
In another: `while true; do cat /tmp/univisal.in.fifo > /tmp/uni; done`
In first term again: `time f`

> real	0m0.004s
> user	0m0.004s
> sys	0m0.000s

This remains broadly the same when running `univisal.py` in the second terminal instead, version at this commit.

## Misc

Note: in vim, counts before an operator multiply with the count after the operator.

In vim, operators leave the cursor to the left of the text operated on.

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

Because Univisal is cross-platform, and written in a well-known language (python), it will be more extensible and easier to write for, so *should* end up with more features/supported actions than vim_ahk.

## OSX

A [handful](https://www.reddit.com/r/vim/comments/56twvs/modal_keybindings_everywhere_with_hammerspoon_mac/) of [Hammerspoon](https://github.com/wingillis/hammerspoon-vim-bindings) vim spoons exist. None are phenominal, most are fine.

## X11

None that I know of, which was the main motivation for writing this.

I just decided that, if I was going to put time into another emulator, I wanted it to be a good one and therefore I wanted to use it on any OS.
Hence, Univisal was born.


# TODO

VisualLine, VisualChar modes

Replace mode?

Record normal commands, insert commands for dot redo?
