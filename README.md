# API-calls-to-ADO

There are several types of ADO queries. In this examples several ones are used:  
1/ List of application (flat)  
2/ Use results of a query saved in ADO (with children)  

How it works:  
1/ List of applications is genereted using a query. 
2/ For each application, we go deeper and get the list of features (each application contains several features)  
3/ For each feautre, we go deeper and get the list of use cases and tasks (each feature contains several use cases which contains several tasks)  
4/ For each task one makes a query to get information about its title and other details  



json formatting in VSCode: 
```
Shift+Alt+F 
```

sources: 
```
https://stackoverflow.com/questions/60341728/is-there-a-way-to-call-azure-devops-via-python-using-requests
```

Doc REST API ADO
```
https://learn.microsoft.com/en-us/rest/api/azure/devops/?view=azure-devops-rest-7.1&viewFallbackFrom=azure-devops-rest-5.1
```

More examples in the link below:
```
https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/list?view=azure-devops-rest-5.0&tabs=HTTP
```
