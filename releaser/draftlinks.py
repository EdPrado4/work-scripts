#! /usr/bin/env python3
"""
Script to get a finding URL based on its ID

Author: oprado@fluidattacks.com

Usage: python3 draftlinks.py {ID}
"""


import json
import sys
import requests
import releaserchecks

TOKEN = releaserchecks.get_asm_token()
HEADERS = {'authorization': f'Bearer {TOKEN}'}
URL = 'https://app.fluidattacks.com/api'

try:
    ID = sys.argv[1]
except IndexError:
    print("No ID was provided")
    sys.exit(1)

def get_group(identifier):
    """
    Get the group of the ID
    """
    query = f'''
        query {{
            finding(identifier:"{identifier}"){{
                groupName
            }}
        }}
    '''
    res = requests.post(URL, headers=HEADERS, json={'query': query})
    json_data = json.loads(res.text)
    try:
        group = json_data['data']['finding']['groupName']
        return group
    except TypeError:
        print("Invalid ID!")
        sys.exit(1)

def get_org(groupname):
    """
    Get the org of the ID
    """
    query2 = f'''
        query {{
            group(groupName:"{groupname}") {{
                organization
            }}
        }}
    '''
    resp = requests.post(URL, headers=HEADERS, json={'query': query2})
    json_data2 = json.loads(resp.text)
    try:
        org = json_data2['data']['group']['organization']
        return org
    except TypeError:
        print("Something went terribly wrong")

CURRENT_GROUP = get_group(ID)
CURRENT_ORG = get_org(CURRENT_GROUP)
print(f'https://app.fluidattacks.com/orgs/{CURRENT_ORG}/groups/{CURRENT_GROUP}/\
        vulns/{ID}/description')
