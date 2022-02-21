#! /usr/bin/env python3

"""
Script to encrypt secret releaser notes ;)
Takes as input the file plain-notes.yaml
Author: oprado@fluidattacks.com
Usage: python3 encrypt.py
"""

from cryptography.fernet import Fernet
import releaserchecks
import sys

KEY = releaserchecks.get_decryption_key(strict=True)
FERNET = Fernet(KEY)

try:
    with open('plain-notes.yaml', 'rb') as file:
        ORIGINAL = file.read()
        file.close()
except FileNotFoundError:
    print("No plain notes to encrypt!")
    sys.exit(1)

ENCRYPTED = FERNET.encrypt(ORIGINAL)

with open('notes.yaml', 'wb') as encrypted_file:
    encrypted_file.write(ENCRYPTED)
    encrypted_file.close()
