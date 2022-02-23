#! /usr/bin/env python3

"""
Script to reject or delete drafts in bulk.
Takes the file 'drafts.lst' as input
the file contains a list of finding IDs, one per line

Author: oprado@fluidattacks.com

Usage: $python3 draftsbulk --rej - To reject vulns in list
       $python3 draftsbulk --del - To delete vulns in list
"""


import sys
from concurrent.futures import ThreadPoolExecutor
import releaserchecks


TOKEN = releaserchecks.get_asm_token()

try:
    MODE = sys.argv[1]
except IndexError:
    print("No mode was provided")
    sys.exit(1)

try:
    with open('drafts.lst', 'r', encoding="utf-8") as DRAFTSID:
        DRAFTS = []
        for ID in DRAFTSID:
            ID = ID.split('\n')
            ID = ''.join(ID)
            DRAFTS.append(ID)
        DRAFTSID.close()
except FileNotFoundError:
    print("Could not find the list of drafts :(")
    sys.exit(1)


def deletedraft(identifier):
    """
    Define the query to delete drafts
    and execute the request
    """
    mutation_delete = f'''
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
    json_data = releaserchecks.request_asm_api(TOKEN, mutation_delete)
    if json_data["data"]:
        print(f"Success, {identifier} deleted!")
    else:
        msg = json_data["errors"][0]["message"]
        if "Access denied" in msg:
            print(f"Draft {identifier} does not exist")
        else:
            print("Unknown error \N{face screaming in fear}")


def rejectdraft(identifier):
    """
    Define the query to reject the draft
    and execute the request
    """
    mutation_reject = f'''
        mutation {{
        rejectDraft(
            findingId: "{identifier}"
        )
        {{
            success
        }}
        }}
    '''

    json_data = releaserchecks.request_asm_api(TOKEN, mutation_reject)
    if json_data["data"]:
        print(f"Success, {identifier} rejected!")
    else:
        msg = json_data["errors"][0]["message"]
        if "The draft has not been submitted yet" in msg:
            print(f"Draft {identifier} has been already rejected")
        elif "Access denied" in msg:
            print(f"Draft {identifier} does not exist or is not submitted")
        else:
            print(f"Unknown error in {identifier} \N{face screaming in fear}")


if MODE == "--rej":
    ThreadPoolExecutor().map(rejectdraft, DRAFTS)
elif MODE == "--del":
    ThreadPoolExecutor().map(deletedraft, DRAFTS)
else:
    print("invalid mode")
    sys.exit(1)
