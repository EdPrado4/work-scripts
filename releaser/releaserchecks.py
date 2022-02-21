#! /usr/bin/env python3

"""
Miscelaneous script to support other releaser scripts
Author: oprado@fluidattacks.com
Usage: No usage, this is just a bunch of functions ;)
"""

import os
import sys

def get_asm_token():
    """
    This function tries to retrieve
    the ASM API token from environment variables
    """
    try:
        token = os.environ["INTEGRATES_API_TOKEN"]
        return token
    except KeyError:
        print("Set the INTEGRATES_API_TOKEN env var first!")
        sys.exit(1)

def get_decryption_key(strict):
    """
    This function tries to retrieve
    the notes decryption key from environment variables
    In strict mode, exits the execution
    """
    try:
        key = os.environ["DECRYPTION_KEY"]
        return key
    except KeyError:
        if strict:
            print("Unable to locate decryption key, quitting ...")
            sys.exit(1)
        else:
            raise KeyError
