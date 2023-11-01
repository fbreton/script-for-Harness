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
var_value = args['Value']
var_desc = args['desc']


#Control that we've the right arguments

headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
}

variable = {
    "variable":{
        "identifier":var_name,
        "name":var_name,
        "description":var_desc,
        "orgIdentifier":org_id,
        "projectIdentifier":proj_id,
        "type":"String",
        "spec": {
            "valueType":"FIXED",
            "type":"string",
            "fixedValue":var_value
        }
    }
}

#Adding the vriable
url = "https://app.harness.io/ng/api/variables?accountIdentifier=" + account_id
response = requests.request("POST",url,data=json.dumps(variable),headers=headers).json()

#If error, provide error message
if response['status'] != "SUCCESS":
    print(response['message'])
    sys.exit(1)
