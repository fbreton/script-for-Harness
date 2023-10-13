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
parser.add_argument('--ReleaseName', help='Release name')
parser.add_argument('--OrgId', help='Organisation Id')
parser.add_argument('--ProjId', help='Project Id')
parser.add_argument('--Service', help='Service Id')
parser.add_argument('--EnvId', help='Environment Id')
parser.add_argument('--api_key', help='api')
args = vars(parser.parse_args())

account_id = args['account']
api_key = args['api_key']
release = args['ReleaseName'].replace(".","_")
release_name = release + "_Status"
org_id = args['OrgId']
proj_id = args['ProjId']
service = args['Service']
env_id = args['EnvId']

#Control that we've the right arguments

headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
}

# release status if it is the first env update
release_status = {
    "env_id":env_id,
    "services": [service]
}

# release variable if it is the first update and variable creation
value = [release_status]
value = json.dumps(value)
release_variable = {
    "variable":{
        "identifier":release_name,
        "name":release_name,
        "description":"Used to manage the deployment status of a release",
        "orgIdentifier":org_id,
        "projectIdentifier":proj_id,
        "type":"String",
        "spec": {
            "valueType":"FIXED",
            "type":"string",
            "fixedValue":value
        }
    }
}

#Getting the variable if already exist
url= "https://app.harness.io/ng/api/variables/?accountIdentifier="+account_id+ "&orgIdentifier=" +org_id+"&projectIdentifier="+proj_id+"&searchTerm="+release_name
response = requests.request("GET", url, headers=headers).json()
data = response['data']
items = data['totalItems']
exist = False
i = 0
while i < items:
    if data['content'][i]['variable']['name'] == release_name:
        release_variable = data['content'][i]
        value = json.loads(release_variable['variable']['spec']['fixedValue'])
        i = items
        exist = True
    i += 1

# Variable does not already exist
url = "https://app.harness.io/ng/api/variables?accountIdentifier="+account_id
if not exist:
    response = requests.request("POST",url,data=json.dumps(release_variable),headers=headers).json()
    if response['status'] != "SUCCESS":
        print(response['message'])
        sys.exit(1)
    print("Service " + service + " tag as deployed in environment " + env_id)
    sys.exit()

# Variable already exist
# Get the environment if deployment already happened for the release in the environment
i = 0
last = len(value)
id_env = last
while i < last:
    if value[i]['env_id'] == env_id:
        id_env = i
        i = last
    i += 1

# No deployment in the env
if id_env == last:
    value.append(release_status)
else:
# Env already had a deployment
    try:
        i = value[id_env]['services'].index(service)
        print("Service " + service + " already tag as deployed in environment " + env_id)
        sys.exit()
    except ValueError:
        value[id_env]['services'].append(service)

# Update the variable
release_variable['variable']['spec']['fixedValue'] = json.dumps(value)
response = requests.request("PUT",url,data=json.dumps(release_variable),headers=headers).json()
if response['status'] != "SUCCESS":
    print(response['message'])
    sys.exit(1)

print("Service " + service + " tag as deployed in environment " + env_id)
