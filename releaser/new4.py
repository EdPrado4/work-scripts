#! /usr/bin/env python3

"""
Script to check Drafts states
Author: oprado@fluidattacks.com
Usage: $ python3 new3.py  - Prints the submitted Drafts
       $ python3 new3,py --rej - Prints the rejected drafts
       $ python3 new3.py --cre - Prints the created drafts
"""

from concurrent.futures import ThreadPoolExecutor
from json.decoder import JSONDecodeError as JE
from functools import partial
import os
import sys
import json
import ast
from requests.exceptions import ConnectionError as CE
import requests
from cryptography.fernet import Fernet, InvalidToken


# Get the key from environmental variable
try:
    KEY = os.environ.get('DECRYPTION_KEY')
    FERNET = Fernet(KEY)
    # Load secrets file
    with open('notes.yaml', 'rb') as enc_file:
        ENCRYPTED = enc_file.read()
        DECRYPTED = FERNET.decrypt(ENCRYPTED)
        DECDATA = DECRYPTED.decode("utf-8")
        DECDATA = DECDATA.split('\n')
        DECDATA = ''.join(DECDATA)
        NOTES = ast.literal_eval(DECDATA)
        enc_file.close()
except TypeError:
    print("You must set the DECRYPTION_KEY env variable")
    sys.exit(1)
except InvalidToken:
    print("The notes seems to be decrypted, careful")
    sys.exit(1)
except SyntaxError:
    print("The notes couldn't be retrieved, is it over encrypted?")
    sys.exit(1)
except FileNotFoundError:
    print("No notes.yaml file was found, notes are not shown")
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

TOKEN = os.environ.get('INTEGRATES_API_TOKEN')
EXCLUDED_PRJ = NOTES["excluded"]

try:
    with open('groups.lst', 'r') as grouplist:
        GROUPS = []
        for member in grouplist:
            member = member.split('\n')
            member = ''.join(member)
            if member not in EXCLUDED_PRJ:
                GROUPS.append(member)
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
    headers = {'authorization': f'Bearer {TOKEN}'}
    url = 'https://app.fluidattacks.com/api'
    try:
        res = requests.post(url, headers=headers, json={'query': query})
        json_data = json.loads(res.text)
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
    except JE:
        print(f'something went wrong with {group}')
    except CE:
        print('Check your shitty connection')


PARTIALGETDRAFTS = partial(get_drafts, DRAFT_TYPE)
ThreadPoolExecutor().map(PARTIALGETDRAFTS, GROUPS)
