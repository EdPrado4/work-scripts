#! /usr/bin/env python3

"""
Script to reject drafts in bulk
Takes as input the file: "to_reject.lst"
with a list of finding ids, one per line

Author: oprado@fluidattacks.com

Usage: python3 rejectbulk.py
"""

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
import requests
import releaserchecks

TOKEN = releaserchecks.get_asm_token()

try:
    with open('to_reject.lst', 'r', encoding="utf-8") as DRAFTSID:
        DRAFTS = []
        for ID in DRAFTSID:
            ID = ID.split('\n')
            ID = ''.join(ID)
            DRAFTS.append(ID)
        DRAFTSID.close()
except FileNotFoundError:
    print("Could not find the list of drafts to reject :(")
    sys.exit(1)


def rejectdraft(identifier):
    """
    Define the query to reject the draft
    and execute the request
    """
    mutation = f'''
        mutation {{
        rejectDraft(
            findingId: "{identifier}"
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
        print(f"Success, {identifier} rejected!")
    else:
        msg = json_data["errors"][0]["message"]
        if "The draft has not been submitted yet" in msg:
            print(f"Draft {identifier} has been already rejected")
        elif "Access denied" in msg:
            print(f"Draft {identifier} does not exist")
        else:
            print(f"Unknown error in {identifier} \N{face screaming in fear}")


ThreadPoolExecutor().map(rejectdraft, DRAFTS)
