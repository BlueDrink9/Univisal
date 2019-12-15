import os
import subprocess
import sys

def get_script_dir():
    # __file__ gets overriden by autokey.service.scriptrunner.execute.
    return os.path.dirname(__file__)

key = engine.get_macro_arguments()[0]
if key is None:
    key = ""
    exit(1)

def univi():
    univi_sh = os.path.join(get_script_dir(), "..", "..", "src", "univi.sh")

    output = subprocess.check_output(["bash", univi_sh, key]).decode()
    engine.set_return_value(output)


univi()
