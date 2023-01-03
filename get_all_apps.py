# api calls to DevOps

import requests
import base64
import pandas as pd


# token_for_azure token
# read only
pat = '***'


authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')


# initialization dataFrame
cols =  ["wi_id", "wi_title", "wi_parent_id", "wi_state"]
df_applications = pd.DataFrame([],  columns = cols)
'''
data = {
    "wi_id": [],
    "wi_title": [],
    "wi_parent_id": [],
    "wi_state": []
}
df_applications = pd.DataFrame(data)
'''



# GET ALL APPS
url = "https://dev.azure.com/go-gl-pr-migfactory-axa365/Migration_Factory/_apis/wit/wiql/759e7933-35ac-452e-bc2d-486796ac539b?api-version=5.1"

headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic '+ authorization
}

response = requests.get(
    url = url,
    headers=headers,
)



def save_working_item_into_data_frame(working_item_id, df_applications): 
    
    """
    Get a working item title, parent, status 
    and saves it into a dataframe
    """

    # url = 'https://dev.azure.com/go-gl-pr-migfactory-axa365/_apis/wit/workItems/3050?$expand=all'
    url = 'https://dev.azure.com/go-gl-pr-migfactory-axa365/_apis/wit/workItems/' + str(working_item_id) + '?$expand=all'

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+ authorization
    }

    response = requests.get(
        url = url,
        headers=headers,
    )

    # working item Title
    wi_title = response.json()["fields"]["System.Title"]

    # working item State
    wi_state = response.json()["fields"]["System.State"]

    # working item Relations
    relations = response.json()["relations"]
    for relation in relations: 
        if relation['rel'] == 'System.LinkTypes.Hierarchy-Reverse':
            # print('Parent')
            raw_id = relation['url']
            start_line = raw_id.find('workItems/') + 10
            parent_id = int(raw_id[start_line:])
            # print(raw_id[start_line:])
            # print('---')


    #load data into a DataFrame object:
    """
    new_row = {
        "wi_id": [wi_id],
        "wi_title": [wi_title],
        "wi_parent_id": [parent_id],
        "wi_state": [wi_state]
    }
    """
    new_row = [wi_id, wi_title, parent_id, wi_state]
    new_df = pd.DataFrame([new_row], columns=cols)

    df_applications = pd.concat([df_applications, new_df], ignore_index = True)
    # df_applications.append(new_row, ignore_index=True)
    # df_applications = df_applications.append(new_row, ignore_index=True)
    return df_applications


# get the 1st WI id
'''
wi_id = response.json()["workItems"][0]["id"]
item_data = save_working_item_into_data_frame(wi_id, df_applications)
print(item_data)
'''

# write to dframe
for i in range(2):
    wi_id = response.json()["workItems"][i]["id"]
    df_applications = save_working_item_into_data_frame(wi_id, df_applications)

print(df_applications)
