# api calls to Azure DevOps

import requests
import base64


# token_for_azure token
# read only
pat = '***'


authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')

# get a WI by ID
url="https://dev.azure.com/go-gl-pr-migfactory-axa365/_apis/wit/workitems?ids=41412&api-version=5.0"

# get list of childs for a WI
# url="https://dev.azure.com/go-gl-pr-migfactory-axa365/_apis/wit/workitems?ids=41414&$expand=all&api-version=5.0"

# get list of apps from an Epic
# url="https://dev.azure.com/go-gl-pr-migfactory-axa365/_apis/wit/workitems?ids=40529&$expand=all&api-version=5.0"
## it doesn't provide app names, only id are available, so have to create additional loop to go deeper and get app name

# display only selected fields
# url="https://dev.azure.com/go-gl-pr-migfactory-axa365/_apis/wit/workitems?ids=40529&fields=System.Id,System.Title&api-version=5.0"


headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic '+authorization
}

response = requests.get(
    url = url,
    headers=headers,
)


print(response.text)
