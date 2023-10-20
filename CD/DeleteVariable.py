import requests
import json
import sys
import argparse
import urllib.parse
from requests import get, post, exceptions

# Get all command line arguments
full_cmd_arguments=sys.argv
argument_list=full_cmd_arguments[1:]
parser = argparse.ArgumentParser()
parser.add_argument('--account', help='Harness Account Id')
parser.add_argument('--OrgId', help='Organisation Id')
parser.add_argument('--ProjId', help='Project Id')
parser.add_argument('--api_key', help='api')
parser.add_argument('--Name',help="Variable Name")
parser.add_argument('--Value',help="Variable Value")
parser.add_argument('--desc',help="Variable Description")

args = vars(parser.parse_args())

account_id = args['account']
api_key = args['api_key']
org_id = args['OrgId']
proj_id = args['ProjId']
var_name = args['Name']


#Control that we've the right arguments
if (proj_id != "") and (org_id == ""):
    print("When project id is defined, organisation id has to be provided")
    sys.exit(1)

headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
}

#Url part if org_id and or proj_id are defined
url_add = ""
if org_id != "":
    url_add = "&orgIdentifier=" + org_id
    if proj_id != "":
        url_add = url_add + "&projectIdentifier=" + proj_id

#Delete the variable
url = "https://app.harness.io/ng/api/variables/" + var_name + "?accountIdentifier=" + account_id + url_add
response = requests.request("DEL",url,headers=headers).json()

#If error, provide error message
if response['status'] != "SUCCESS":
    print(response['message'])
    sys.exit(1)
