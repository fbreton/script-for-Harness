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
parser.add_argument('--ProjId', help='Project Id')
parser.add_argument('--FromEnvId', help='Environment Id on which all have to be deployed before next env')
parser.add_argument('--ToEnvId', help='Environment Id on for next deployment')
parser.add_argument('--api_key', help='api')
parser.add_argument('--AvailFile', help='Release Availability json file path')


args = vars(parser.parse_args())

account_id = args['account']
api_key = args['api_key']
def_release = args['ReleaseName']
def_release_name = def_release.replace(".","_") + "_Status"
org_id = args['OrgId']
proj_id = args['ProjId']
from_env_id = args['FromEnvId']
to_env_id = args['ToEnvId']
avail_file = urllib.parse.quote(urllib.parse.quote("/"+ def_release + "/" + args['AvailFile'], safe=''))

#Control that we've the right arguments

headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
}

#get the service required for a release to move to next env
url = "https://app.harness.io/ng/api/file-store/files/" + avail_file + "/content?accountIdentifier=" + account_id + "&orgIdentifier=" + org_id + "&projectIdentifier=" + proj_id
try: 
  dep_to_wait = json.loads(requests.request("GET", url, headers=headers).json()['data'])
except:
  print("Done")
  sys.exit()

#remove from waiting list what is already deployed for each app
idx_appw = 0
for appWait in dep_to_wait:
  try:
    release = appWait['ReleaseName']
    release_name = release.replace(".","_") + "_Status"
  except KeyError:
    release = def_release
    release_name = def_release_name
  #get what is deplloyed for appWait
  url= "https://app.harness.io/ng/api/variables/" + release_name + "?accountIdentifier=" + account_id + "&orgIdentifier=" + org_id + "&projectIdentifier=" + appWait['appId']
  response = requests.request("GET", url, headers=headers).json()
  if response['status'] == "SUCCESS":
    data = json.loads(response['data']['variable']['spec']['fixedValue'])
    if appWait['appId'] == proj_id:
      envsearch = from_env_id
    else:
      envsearch = to_env_id
    servDep = []
    for appDep in data:
      if appDep['env_id'] == envsearch:
        servDep = appDep['services']
    for serv in servDep:
      try:
        idx_servw = appWait['services'].index(serv)
        dep_to_wait[idx_appw]['services'].pop(idx_servw)
      except ValueError:
        pass
  idx_appw += 1

# we informe about the status of the waiting dépendencies
dep = False
for appWait in dep_to_wait:
  nb_serv = len(appWait['services'])
  if nb_serv > 0:
    if appWait['appId'] == proj_id:
      envsearch = from_env_id
    else:
      envsearch = to_env_id
    if nb_serv == 1:
      text = "Service " + ','.join(appWait['services']) +  " is"
    else:
      text = "Services " + ','.join(appWait['services']) + " are"
    print(text + " still not deployed in environment " + envsearch + " for application " + appWait['appId'])
    dep = True
if not dep:
  print("Done")
