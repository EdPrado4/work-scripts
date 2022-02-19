#! /usr/bin/env python3

"""
Script to get the releaser notes on plaintext
Author: oprado@fluidattacks.com
Usage: $python3 decrypt.py
"""

import os
import sys
from cryptography.fernet import Fernet, InvalidToken

try:
    KEY = os.environ.get('DECRYPTION_KEY')
    FERNET = Fernet(KEY)
except TypeError:
    print("You must set a valid DECRYPTION_KEY env variable")
    sys.exit(1)


with open('notes.yaml', 'rb') as enc_file:
    ENCRYPTED = enc_file.read()
    enc_file.close()

try:
    DECRYPTED = FERNET.decrypt(ENCRYPTED)
except InvalidToken:
    print("The file has already been decrypted!")
    sys.exit(1)

with open('notes.yaml', 'wb') as decrypted_file:
    decrypted_file.write(DECRYPTED)
    decrypted_file.close()
