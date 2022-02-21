#! /usr/bin/env python3

"""
Script to get the releaser notes on plaintext
Author: oprado@fluidattacks.com
Usage: $python3 decrypt.py
"""

from email.policy import strict
import sys
from cryptography.fernet import Fernet, InvalidToken
import releaserchecks

KEY = releaserchecks.get_decryption_key(strict=True)
FERNET = Fernet(KEY)

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
