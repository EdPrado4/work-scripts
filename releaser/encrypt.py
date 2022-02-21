#! /usr/bin/env python3

"""
Script to encrypt secret releaser notes ;)
Author: oprado@fluidattacks.com
Usage: python3 encrypt.py
"""

from email.policy import strict
from cryptography.fernet import Fernet
import releaserchecks

KEY = releaserchecks.get_decryption_key(strict=True)
FERNET = Fernet(KEY)


with open('notes.yaml', 'rb') as file:
    ORIGINAL = file.read()
    file.close()

# encrypting the file
ENCRYPTED = FERNET.encrypt(ORIGINAL)

# writing the encrypted data
with open('notes.yaml', 'wb') as encrypted_file:
    encrypted_file.write(ENCRYPTED)
    encrypted_file.close()
