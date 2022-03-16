#! /usr/bin/env python3

"""
Script to create the list of accesible groups
according to your role
This script is an input for the new4.py script

Author: oprado@fluidattacks.com

Usage: $ python3 update_groups.py

"""


import json
import os
import concurrent.futures
from json.decoder import JSONDecodeError as JE
from requests.exceptions import ConnectionError as CE
import requests
import releaserchecks


try:
    os.remove('groups.lst')
    print("Old list deleted, generating a new list ...")
except FileNotFoundError:
    print('nice! \N{smirking face} creating a brand new list')

API_TOKEN = releaserchecks.get_asm_token()


def get_orgs():
    """
    Get all the organizations the user has access
    """
    query_org = '''
      query {
        me {
          organizations {
            name
          }
        }
      }
    '''
    all_orgs = []
    json_data = releaserchecks.request_asm_api(API_TOKEN, query_org)
    orgs = json_data['data']['me']['organizations']
    for org in orgs:
        all_orgs.append(org['name'])
    return all_orgs


ORGS = get_orgs()

ERRORS = []


def get_groups(org):
    """
    Get all the groups the user has access
    """
    headers = {'authorization': f'Bearer {API_TOKEN}'}
    url = 'https://app.fluidattacks.com/api'
    query = f"""
    query {{
      organizationId(organizationName: "{org}"){{
        groups{{
          name
        }}
      }}
    }}
    """
    try:
        res = requests.post(url, headers=headers, json={'query': query})
        json_data = json.loads(res.text)
        groups = json_data['data']['organizationId']['groups']
        for group in groups:
            with open('groups.lst', 'a+', encoding='utf-8') as groupfile:
                groupfile.write(group['name']+'\n')
                groupfile.close()

    except CE:
        print("oops, something went wrong")
    except JE:
        print(f"Something went wrong while checking {org}")
        ERRORS.append(org)


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(get_groups, ORGS)

if ERRORS:
    print("Retrying orgs with ERRORS:")
    print(ERRORS)
    with concurrent.futures.ThreadPoolExecutor() as execERRORS:
        execERRORS.map(get_groups, ERRORS)
print("Done!")
