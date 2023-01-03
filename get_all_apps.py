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

    new_row = [working_item_id, wi_title, parent_id, wi_state]
    new_df = pd.DataFrame([new_row], columns=cols)
    
    # load data into a DataFrame object:
    df_applications = pd.concat([df_applications, new_df], ignore_index = True)

    return df_applications


def show_children(parent_id):
    """
    Generates list of children_ids based on parent_id
    """
    url = 'https://dev.azure.com/go-gl-pr-migfactory-axa365/_apis/wit/workItems/' + str(parent_id) + '?$expand=all'

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+ authorization
    }

    response = requests.get(
        url = url,
        headers=headers,
    )

    # where ids of children will be stored
    list_of_children = []

    # working item Relations
    relations = response.json()["relations"]
    for relation in relations: 
        if relation['rel'] == 'System.LinkTypes.Hierarchy-Forward':
            # print('Child')
            raw_id = relation['url']
            start_line = raw_id.find('workItems/') + 10
            child_id = int(raw_id[start_line:])
            list_of_children.append(child_id)
    
    return list_of_children



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

# list(list of dictionaries) of all the applications
# applications = response.json()["workItems"][i]["id"]
n = 2
applications = response.json()["workItems"]#[i]["id"]
applications = applications[:n]
# print(applications)


for i in range(len(applications)):
    # go through all(n) the apps
    # wi_id = response.json()["workItems"][i]["id"]
    # print(application)
    application_id = applications[i]["id"]
    feature_ids = show_children(application_id)
    for feature_id in feature_ids:
        user_stories = show_children(feature_id)
        for user_story in user_stories:
            tasks = show_children(user_story)
            for task in tasks:
                df_applications = save_working_item_into_data_frame(task, df_applications)
                # print(task)
                # df_applications.to_csv('file_name.csv')
    # print(df_applications)

df_applications.to_csv('file_name_2.csv')
