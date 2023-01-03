# api calls to DevOps

import requests
import base64
import pandas as pd


# token_for_azure token
# read only
pat = '***'


authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')



# GET ALL APPS
url = "https://dev.azure.com/go-gl-pr-migfactory-axa365/Migration_Factory/_apis/wit/wiql/759e7933-35ac-452e-bc2d-486796ac539b?api-version=5.1"

headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic '+authorization
}

response = requests.get(
    url = url,
    headers=headers,
)

# get the 1st WI id
wi_id = response.json()["workItems"][0]["id"]



# GET TITLE, PARENT, CHILD ETC. FOR EACH APP
url = 'https://dev.azure.com/go-gl-pr-migfactory-axa365/_apis/wit/workItems/3050?$expand=all'

headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic '+authorization
}

response = requests.get(
    url = url,
    headers=headers,
)

# print(response.text)

# Title
wi_title = response.json()["fields"]["System.Title"]

# State
wi_state = response.json()["fields"]["System.State"]

# Relations
relations = response.json()["relations"]
for relation in relations: 
    if relation['rel'] == 'System.LinkTypes.Hierarchy-Reverse':
        # print('Parent')
        raw_id = relation['url']
        start_line = raw_id.find('workItems/') + 10
        parent_id = int(raw_id[start_line:])
        # print(raw_id[start_line:])
        # print('---')


data = {
  "wi_id": [wi_id],
  "wi_title": [wi_title],
  "wi_parent_id": [parent_id],
  # "wi_child_id": [child_id],
  "wi_state": [wi_state]
}

#load data into a DataFrame object:
df = pd.DataFrame(data)

# print the dataFrame
print(df)


# test.append(['James', '95', 'M'])

