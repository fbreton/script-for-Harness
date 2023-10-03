# Description of usage of the scripts
Those script are used on some use case of Harness CCM Asset Management. Here the goal is to document their usage and associated use cases.

## CreateUpdateBucket.py
This script can be call used in a pipeline called by an asset management rule to create or update a Cost Category and associated Cost Bucket that will be used to show the cost of assets 
matching the asset governance rule.

Command to launch it ( with the right value in the variables):
```
python3 createCBucket.py --account "$account" --api_key "$api_key" --CCName "$CCName" --CBName "$CBName" --Scope "$Scope" --Region "$Region" --fieldName "$fieldName" --Values "$Values"
```
**account**: Harness account id  
**api_key**: Harness api key  
**CCName**: Cost Category name  
**CBName**: Cost Bucket name  
**Scope**: Cloud (AZURE, AWS)  
**Region**: the region of the asset
**fieldName**: name of the field on which to filter ("Instance Id" for exemple)  
**Values**: the result of the asset rule, so typically a list of values to filter for the fieldName

The following is an asset governance rule exemple that calls an Harness pipeline containing a step to run the script:

````
 policies:
  - name: orphaned-disk
    resource: azure.disk
    filters:
      - type: value
        key: properties.diskState
        value: "Unattached"
    actions:
        - type: webhook
          url: "https://app.harness.io/gateway/pipeline/api/webhook/custom/v2?accountIdentifier=string&orgIdentifier=string&projectIdentifier=stringx&pipelineIdentifier=string&triggerIdentifier=string"
          batch: true
          body: |-
            {
                "CCName": 'Unused Assets',
                "CBName": 'Azure Unattached Disk',
                "Scope": 'AZURE',
                "fieldName": 'Instance id',
                "Values": resources[].id,
                "Region": resources[0].location
            }
```
