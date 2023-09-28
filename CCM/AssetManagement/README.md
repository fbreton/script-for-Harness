# Description of usage of the scripts
Those script are used on some use case of Harness CCM Asset Management. Here the goal is to document their usage and associated use cases.

## CreateUpdateBucket.py
This script can be call used in a pipeline called by an asset management rule to create or update a Cost Category and associated Cost Bucket that will be used to show the cost of assets 
matching the asset governance rule.

Command to launch it ( with the right value in the variables):
```
python3 createCBucket.py --account "$account" --api_key "$api_key" --CCName "$CCName" --CBName "$CBName" --Scope "$Scope" --fieldName "$fieldName" --Values "$Values"
```
account: Harness account id  
api_key: Harness api key  
CCName: Cost Category name  
CBName: Cost Bucket name  
Scope: Cloud (AZURE, AWS)  
fieldName: name of the field on which to filter ("Instance Id" for exemple)  
Values: the result of the asset rule, so typically a list of values to filter for the fieldName  
