#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import os
import sys

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
