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

#Getting the variable if already exist and exit if not
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
if not exist:
    print("Service " + service + " has not been tagged a deployed in environment " + env_id)
    sys.exit()

# the variable exit
# Get the environment if deployment already happened for the release in the environment
i = 0
last = len(value['environments'])
id_env = last
while i < last:
    if value['environments'][i]['env_id'] == env_id:
        id_env = i
        i = last
    i += 1

# No deployment in the env
if id_env == last:
    print("Service " + service + " has not been tagged a deployed in environment " + env_id)
    sys.exit()

# Env already had a deployment
try:
    i = value['environments'][id_env]['services'].index(service)
    value['environments'][id_env]['services'].pop(i)
    release_variable['variable']['spec']['fixedValue'] = json.dumps(value)
    response = requests.request("PUT",url,data=json.dumps(release_variable),headers=headers).json()
    if response['status'] != "SUCCESS":
        print(response['message'])
        sys.exit(1)
    print("Service " + service + " untag as deployed in environment " + env_id)
except ValueError:
    print("Service " + service + " has not been tagged a deployed in environment " + env_id)

