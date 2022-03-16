#! /usr/bin/env python3

'''
Script to check  if a group has open eventualities
author: oprado@fluidattacks.com

Usage: hasEvents.py {GROUPNAME}
'''

import sys
import releaserchecks

try:
    GROUP = sys.argv[1]
except IndexError:
    print("You must provide the Group name")
    sys.exit(1)

TOKEN = releaserchecks.get_asm_token()

QUERY = f'''
query{{
    group(groupName:"{GROUP}") {{
    events {{
        eventStatus
    }}
    }}
}}
'''
EVENTDATA = releaserchecks.request_asm_api(TOKEN, QUERY)
try:
    for event in EVENTDATA["data"]["group"]["events"]:
        if event["eventStatus"] == "CREATED":
            print(f"{GROUP} has open events \N{loudly crying face}")
            sys.exit(0)
except TypeError:
    print("Invalid Group!")
    sys.exit(1)
print(f"{GROUP} has not any open event \N{smiling face with sunglasses}")
