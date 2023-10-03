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
parser.add_argument('--CCName', help='Cost Category Name')
parser.add_argument('--CBName', help='Cost Bucket Name')
parser.add_argument('--Scope', help='Kind of Cloud')
parser.add_argument('--Region', help='region')
parser.add_argument('--fieldName', help='fieldName to filter on')
parser.add_argument('--Values', help='Values to filter on')
parser.add_argument('--api_key', help='api')
args = vars(parser.parse_args())
account_id = args['account']
Region = args['Region']

CCName = args['CCName']
CCNameSearch = urllib.parse.quote(CCName)
CBName = args['CBName'] + " - " + Region
Scope = args['Scope']
fieldName = args['fieldName']
Values = args['Values'].replace('[','').replace(']','').split(',')
api_key = args['api_key']

headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
}

# Field mapping based on Scope and fieldName
if Scope == "AZURE":
    idName = "Azure"
    if fieldName == "Instance id":
        fieldId = "azureInstanceId"
    else:
        print("field name " + fieldName + "not supported")
        sys.exit(1)
elif Scope == "AWS":
    print("AWS not already implemented")
    sys.exit(1)
elif Scope == "GCP":
    print("GCP not already implemented")
    sys.exit(1)
else:
    print(Scope + "not supported")
    sys.exit(1)

# if no resources,then we can exit
if  Values == []:
    print("No " + fieldName + " provided so we won't update the Cost Category " + CCName)
    sys.exit()

# Cost Bucket definition
costBucket= {
            "name":CBName,
            "rules":[
                {
                    "viewConditions":[
                        {
                            "type":"VIEW_ID_CONDITION",
                            "viewField":{
                                "fieldId":fieldId,
                                "fieldName":fieldName,
                                "identifier":Scope,
                                "identifierName":idName
                            },
                            "viewOperator":"IN",
                            "values":Values
                        }
                    ]
                }
            ]
        }

# Cost Category definition if new one
defaultdata={
    "name":CCName,
    "accountId":account_id,
    "costTargets":[costBucket],
    "sharedCosts":None,
    "unallocatedCost":{
        "strategy":"DISPLAY_NAME",
        "label":"Unattributed",
        "sharingStrategy":None,
        "splits":None
    }
}

# Getting the Cost category definition if exist
url = "https://app.harness.io/ccm/api/business-mapping?accountIdentifier="+account_id+"&searchKey="+CCNameSearch
response = requests.request("GET", url, headers=headers)
data = response.json()

# Add new cost category if doesn't exist
url = "https://app.harness.io/ccm/api/business-mapping?accountIdentifier="+account_id
if data["resource"]["totalCount"] == 0:
    data_json = json.dumps(defaultdata)
    response = requests.request("POST", url, data=data_json, headers=headers)
    print("Creating Cost Category -" + CCName + "- with Cost Bucket -" + CBName + "-")
else:
    i=0
    last = len(data["resource"]["businessMappings"][0]["costTargets"])
    cb_id = last
    # Check if cost bucket already exist in the cost category
    while i < last:
        if data["resource"]["businessMappings"][0]["costTargets"][i]["name"] == CBName:
            cb_id = i
            i = last
        i += 1
    # doesn't exit, so adding the new cost bucket
    if cb_id == last:
        data["resource"]["businessMappings"][0]["costTargets"].append(costBucket)
        print("Adding Cost Bucket -" + CBName + "- to Cost Category -" + CCName + "-")
    else:
    # already exist, so replacing it
        data["resource"]["businessMappings"][0]["costTargets"][cb_id] = costBucket
        print("Modifying Cost Bucket -" + CBName + "- into Cost Category -" + CCName + "-")
    data_json = json.dumps(data["resource"]["businessMappings"][0])
    response = requests.request("PUT", url, data=data_json, headers=headers)

response=response.json()["responseMessages"]
if response != []:
    print(response[0]["message"])
    sys.exit(1)
