#! /usr/bin/env python3

'''
Script to check  if a group has open eventualities
author: oprado@fluidattacks.com

Usage: hasEvents.py {GROUPNAME}
'''

import json
import sys
import os
from json.decoder import JSONDecodeError
import requests
import releaserchecks

try:
    GROUP = sys.argv[1]
except IndexError:
    print("You must provide the Group name")
    sys.exit(1)

TOKEN = releaserchecks.get_asm_token()
URL = "https://app.fluidattacks.com/api"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


try:
    QUERY = f'''
    query{{
      group(groupName:"{GROUP}") {{
        events {{
          eventStatus
        }}
      }}
    }}
    '''
    RESP = requests.post(URL, headers=HEADERS, json={'query': QUERY})
    EVENTDATA = json.loads(RESP.text)
    for event in EVENTDATA["data"]["group"]["events"]:
        if event["eventStatus"] == "CREATED":
            print(f"{GROUP} has open events \N{loudly crying face}")
            sys.exit(0)
    print(f"{GROUP} has not any open event \N{smiling face with sunglasses}")
except ConnectionError:
    print("Something went wrong while trying to connect")
    sys.exit(1)
except TypeError:
    print("You either don't have access or the group don't exist")
    sys.exit(1)
except JSONDecodeError:
    print("Unknown error")
    sys.exit(1)
