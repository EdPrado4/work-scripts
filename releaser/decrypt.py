#! /usr/bin/env python3

"""
Script to get the releaser notes on plaintext
The secrets are printed in the plain-notes.yaml file
the secrets are not versioned for security
Author: oprado@fluidattacks.com
Usage: $python3 decrypt.py
"""

from cryptography.fernet import Fernet
import releaserchecks

KEY = releaserchecks.get_decryption_key(strict=True)
FERNET = Fernet(KEY)

with open('notes.yaml', 'rb') as enc_file:
    ENCRYPTED = enc_file.read()
    enc_file.close()

DECRYPTED = FERNET.decrypt(ENCRYPTED)

with open('plain-notes.yaml', 'wb') as decrypted_file:
    decrypted_file.write(DECRYPTED)
    print('plain-notes.yaml file was generated!')
    decrypted_file.close()
