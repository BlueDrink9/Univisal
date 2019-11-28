import os
import subprocess
import sys

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

key = engine.get_macro_arguments()[0]
if key is None:
    key = ""
    exit(1)

def univi():
    univi_sh = os.path.join(get_script_path(), "..", "..", "src", "univi.sh")

    output = subprocess.check_output(["bash", univi_sh, key]).decode()
    engine.set_return_value(output)


univi()
