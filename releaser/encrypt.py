#! /usr/bin/env python3

"""
Script to encrypt secret releaser notes ;)
Author: oprado@fluidattacks.com
Usage: python3 encrypt.py
"""

import os
import sys
from cryptography.fernet import Fernet


try:
    KEY = os.environ.get('DECRYPTION_KEY')
    FERNET = Fernet(KEY)
except TypeError:
    print("You must set a valid DECRYPTION_KEY env variable")
    sys.exit(1)

with open('notes.yaml', 'rb') as file:
    ORIGINAL = file.read()
    file.close()

# encrypting the file
ENCRYPTED = FERNET.encrypt(ORIGINAL)

# writing the encrypted data
with open('notes.yaml', 'wb') as encrypted_file:
    encrypted_file.write(ENCRYPTED)
    encrypted_file.close()
