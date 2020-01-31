# Writing adapters

## Generating adapters

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

## mappings.json

This is a simple json with values as the representation of any special keys for the adapter, eg `{escape}` for autohotkey. Keys are the string univisal uses for that key, as found in the table under **Key representations**.

Any key without an adapter map will be send as the input string.


## Key representations (documentation under construction).

Univisal tries to use the same representation as vim keycodes in `:h intro`, for example in mappings (`:inoremap jj <Esc>`). 
This means they can be inserted using `^V`.
Exceptions are keys that send their non-whitespace text representation when pressed, like `|` (`<Bar>`).

The representations are also only lowercase.

Modifier keys are their standard name, since vim normally only maps them with another key, e.g. <shift>.

Any other keys are listed here. If a key doesn't appear, let me know (because I have forgotten to add it). It should follow the general pattern shown here.

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


