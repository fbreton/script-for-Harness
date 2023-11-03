# Description

Those script has been written to be used in a context of release management to manage service deployment dependencies when those services that are part of a same release are deployed by independant pipelines. This has been done to answer to the following constraints when a release is deployed accross different environments:
- All dependencies of a service must be deployed before it can be deployed in an environment,
- All services of a release have to be ready to be deployed in production before the release can be deployed in production,
- if the release of an application, A, is dependant of another application, B (with specidfic release), then for A can be ready for deployment in production, B has to be already in production
- When an application release is ready to be deployed in production, a Jira ticket has to be opened and its approval will automatically launch the deployment in production

This can be illustrated with the following pipeline:  
![CD pipeline](pipeline.png "CD pipeline")  

With deployment stage beeing like:  
![CD pipeline](deployment.png "CD pipeline")