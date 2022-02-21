#! /usr/bin/env python3

"""
Scrypt to delete drafts in bulk
Takes as input a file: "to_delete.lst"
with a list of ids, one per line

Author: oprado@fluidattacks.com
Usage: $ deletebulk.py
"""

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
import requests
import releaserchecks

TOKEN = releaserchecks.get_asm_token()

try:
    with open('to_delete.lst', 'r', encoding="utf-8") as DRAFTSID:
        DRAFTS = []
        for ID in DRAFTSID:
            ID = ID.split('\n')
            ID = ''.join(ID)
            DRAFTS.append(ID)
        DRAFTSID.close()
except FileNotFoundError:
    print("Could not find the list of drafts to delete :(")
    sys.exit(1)


def deletedraft(identifier):
    """
    Define the query to delete drafts
    and execute the request
    """
    mutation = f'''
    mutation{{
        removeFinding(
        findingId:"{identifier}",
        justification: NOT_REQUIRED
      )
      {{
        success
      }}
    }}
    '''

    url = "https://app.fluidattacks.com/api"
    headers = {
        'authorization': f'Bearer {TOKEN}'
    }
    req = requests.post(url=url, headers=headers, json={'query': mutation})
    json_data = json.loads(req.text)
    if json_data["data"]:
        print(f"Success, {identifier} deleted!")
    else:
        msg = json_data["errors"][0]["message"]
        if "Access denied" in msg:
            print(f"Draft {identifier} does not exist")
        else:
            print("Unknown error \N{face screaming in fear}")


if len(sys.argv) > 1:
    DELETEME = sys.argv[1]
    deletedraft(DELETEME)
else:
    ThreadPoolExecutor().map(deletedraft, DRAFTS)
