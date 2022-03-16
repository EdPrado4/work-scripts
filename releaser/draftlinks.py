#! /usr/bin/env python3
"""
Script to get a finding URL based on its ID

Author: oprado@fluidattacks.com

Usage: python3 draftlinks.py {ID}
"""


import sys
import releaserchecks

TOKEN = releaserchecks.get_asm_token()

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
    json_data = releaserchecks.request_asm_api(TOKEN, query)
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
    json_data2 = releaserchecks.request_asm_api(TOKEN, query2)
    try:
        org = json_data2['data']['group']['organization']
        return org
    except TypeError:
        print("Something went terribly wrong")
        sys.exit(1)


CURRENT_GROUP = get_group(ID)
CURRENT_ORG = get_org(CURRENT_GROUP)
DRAFT_URL = (
    f'https://app.fluidattacks.com/orgs/{CURRENT_ORG}/'
    f'groups/{CURRENT_GROUP}/vulns/{ID}/description'
    )
print(DRAFT_URL)
