# Description

The [Harness.io](https://www.harness.io/products/continuous-delivery "World's Most Advanced CD Platform") template you'll find here have been created to be used in a context of release management to manage service deployment dependencies when those services that are part of a same release are deployed by independant pipelines.  

This has been done to answer to the following constraints when a release is deployed accross different environments:
- All dependencies of a service must be deployed before it can be deployed in an environment,
- All services of a release have to be ready to be deployed in production before the release can be deployed in production,
- if the release of an application, A, is dependant of another application, B (with specidfic release), then for A can be ready for deployment in production, B has to be already in production
- When an application release is ready to be deployed in production, a Jira ticket has to be opened and its approval will automatically launch the deployment in production

To ilustrate the usage, you've also 2 pipeline definitions that deploy 2 services, one being dependent of the other, representing an application APP1 that is contained in a project with the same name.

# Templates

## CreateVariable.yaml

This template is a ShellScript step template that creates an harness string variable at project level and requires the following inputs:  

**API**: API token to access to the project - mandatory  
**VARNAME**: Variable name/id to be created - mandatory  
**VARVALUE**: String value to allocate to the variable - mandatory  
**VARDESC**: description to associate to the variable  


## DeleteVariable.yaml

This template is a ShellScript step template that removes a variable at the project level and requires the followin inputs:  

**API**: API token to access to the project - mandatory  
**VARNAME**: Variable name/id to be removed - mandatory  

## MarkAsDeployed.yaml

This template is a step group template that adds the service identifier of the deployement stage in which it is used to the list of services deployed for a specific release to the environment of the deployment stage. It requires the following inputs:  

**ReleaseName**: The release name for which the service deployed is part of - mandatory  
**ApiKey**: API token to access to the project - mandatory  

## UncheckService.yaml

This template is a step group template that removes the service identifier of the deployement stage in which it is used to the list of services deployed for a specific release to the environment of the deployment stage. It requires the following inputs:  

**RELEASE**: The release name for which the service removed was part of - mandatory  
**API**: API token to access to the project - mandatory  

## WaitDependencies.yaml

This template is a CustomApproval step template that wait until the dependencies requiered by the service, that is deployed in the deployement stage in which it is used, to be declared as deployed. It requires the following inputs:  

**RELEASE**: The release name for which the service to be deployed is part of - mandatory  
**API**: API token to access to the project - mandatory  

