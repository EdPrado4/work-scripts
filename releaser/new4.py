#! /usr/bin/env python3

"""
Script to check Drafts states
Author: oprado@fluidattacks.com
Usage: $ python3 new3.py  - Prints the submitted Drafts
       $ python3 new3,py --rej - Prints the rejected drafts
       $ python3 new3.py --cre - Prints the created drafts
"""

from concurrent.futures import ThreadPoolExecutor
from functools import partial
import sys
import ast
from cryptography.fernet import Fernet
import releaserchecks


# Get the key from environmental variable
try:
    KEY = releaserchecks.get_decryption_key(strict=False)
    FERNET = Fernet(KEY)
    # Load secrets file
    with open('notes.yaml', 'rb') as enc_notes:
        ENCRYPTED = enc_notes.read()
        DECRYPTED = FERNET.decrypt(ENCRYPTED)
        DECDATA = DECRYPTED.decode("utf-8")
        DECDATA = DECDATA.split('\n')
        DECDATA = ''.join(DECDATA)
        NOTES = ast.literal_eval(DECDATA)
        enc_notes.close()
except SyntaxError:
    print("The notes couldn't be retrieved, is it over encrypted?")
    sys.exit(1)
except (FileNotFoundError, KeyError):
    print("No notes.yaml or key was found, notes are not shown")
    NOTES = {'excluded': []}

# Define draft types
DRAFT_TYPE = ''
if len(sys.argv) > 1:
    if sys.argv[1] == '--rej':
        DRAFT_TYPE = 'REJECTED'
    if sys.argv[1] == '--cre':
        DRAFT_TYPE = 'CREATED'
else:
    DRAFT_TYPE = 'SUBMITTED'

TOKEN = releaserchecks.get_asm_token()
EXCLUDED_PRJ = NOTES["excluded"]

try:
    with open('groups.lst', 'r', encoding='utf-8') as grouplist:
        GROUPS = []
        for MEMBER in grouplist:
            MEMBER = MEMBER.split('\n')
            MEMBER = ''.join(MEMBER)
            if MEMBER not in EXCLUDED_PRJ:
                GROUPS.append(MEMBER)
        grouplist.close()
except FileNotFoundError:
    print("No groups list found in the current directory :(")
    sys.exit(1)


def get_drafts(drafttype, group):
    """
    Get the pending, rejected or created drafts
    """
    query = f'''
      query {{
        group(groupName:"{group}") {{
          drafts {{
           groupName
           title
           id
           analyst
           severityScore
           currentState
           reportDate
          }}
        }}
      }}
    '''
    json_data = releaserchecks.request_asm_api(TOKEN, query)
    drafts = json_data['data']['group']['drafts']
    if drafts:
        for draft in drafts:
            if draft['currentState'] == drafttype:
                msg = (
                    f"({draft['groupName']} , {draft['title']}, "
                    f"{draft['severityScore']}, {draft['id']} , "
                    f"{draft['analyst']}, {draft['currentState']}) "
                    f"{draft['reportDate']}"
                )
                print(msg)
                if draft['groupName'] in NOTES:
                    print(f'^ {NOTES[draft["groupName"]]}')


PARTIALGETDRAFTS = partial(get_drafts, DRAFT_TYPE)
ThreadPoolExecutor().map(PARTIALGETDRAFTS, GROUPS)
