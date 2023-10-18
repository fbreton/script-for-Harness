import requests
import json
import sys
import argparse
import time
import urllib.parse
from requests import get, post, exceptions

# Get all command line arguments
full_cmd_arguments=sys.argv
argument_list=full_cmd_arguments[1:]
parser = argparse.ArgumentParser()
parser.add_argument('--account', help='Harness Account Id')
parser.add_argument('--ReleaseName', help='Release name')
parser.add_argument('--OrgId', help='Organisation Id')
parser.add_argument('--Service', help='Service Id')
parser.add_argument('--EnvId', help='Environment Id')
parser.add_argument('--api_key', help='api')
parser.add_argument('--dependencies', help='json for dependencies')
parser.add_argument('--pollTime', help='Time between each poll of the deployment status')

args = vars(parser.parse_args())

account_id = args['account']
api_key = args['api_key']
def_release = args['ReleaseName'].replace(".","_")
def_release_name = def_release + "_Status"
org_id = args['OrgId']
service = args['Service']
env_id = args['EnvId']
dependencies = args['dependencies']
pollTime = int(args['pollTime'])

#Control that we've the right arguments

headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
}

#Check there's some dependencies to check
dep = True
if (dependencies is None) or (dependencies == "null"):
    dep = False
else:
    dep_to_wait = []
    dependencies = json.loads(dependencies)
    last = len(dependencies)
    i=0
    while i < last:
        if len(dependencies[i]['services']) > 0:
            dep_to_wait.append(dependencies[i])
        i += 1
    if dep_to_wait == []:
        dep = False
if not dep:
    print("No dependencies to check to deploy service " + service +" in environment " + env_id)
    sys.exit()

# There is dependencies to check so we loop until there's no more dependencies
while dep_to_wait != []:
    indx_dptw = 0
    last = len(dep_to_wait)
    while indx_dptw < last:
        
        # First we load the deploiment status for project
        depApp = dep_to_wait[indx_dptw]
        try:
            release = depApp['ReleaseName']
            release_name = release.replace(".","_") + "_Status"
        except KeyError:
            release_name = def_release_name
            release = def_release
        url= "https://app.harness.io/ng/api/variables/?accountIdentifier="+account_id+ "&orgIdentifier=" +org_id+"&projectIdentifier="+depApp['appId']+"&searchTerm="+release_name
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
        
        # Then we remove the servise already deployed from the waiting list
        if exist:
            i = 0
            last_dep = len(value)
            while i < last_dep:
                if value[i]['env_id'] == env_id:
                    for serv_dep in value[i]['services']:
                        try:
                            idx_serv_dev = depApp['services'].index(serv_dep)
                            dep_to_wait[indx_dptw]['services'].pop(idx_serv_dev)
                        except ValueError:
                            pass
                    i = last_dep
                i += 1
        if dep_to_wait[indx_dptw]['services'] == []:
            last -= 1
            dep_to_wait.pop(indx_dptw)
        else:
            indx_dptw += 1
    
    # we informe about the status of the waiting dépendencies
    if dep_to_wait != []:
        print("Waiting for the following services to be deployed in environment " + env_id + ":")
        i = 1
        for dep_inst in dep_to_wait:
            j = 1
            for serv_inst in dep_inst['services']:
                try:
                    release = dep_inst['ReleaseName']
                    release_name = release.replace(".","_") + "_Status"
                except KeyError:
                    release_name = def_release_name
                    release = def_release
                idx = i * j
                print("   " + str(idx) + ". " + serv_inst + " from application " + dep_inst['appId'] + " release " + release)
                j += 1
            i += 1
        time.sleep(pollTime)
    else:
        print("All dependencies for service " + service + "are tagged as being deployed in environment " + env_id)