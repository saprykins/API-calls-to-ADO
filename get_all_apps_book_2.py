# api calls to DevOps
# helps to get applications from Azure DevOps

import requests
import base64
import pandas as pd


# token_for_azure token
pat = '***'
authorization = str(base64.b64encode(bytes(':'+pat, 'ascii')), 'ascii')

# initialization dataFrame
# cols =  ["wi_id", "wi_title", "wi_parent_id", "wi_state"]
#
#
#
cols =  ["id", "title", "parent_id", "state", "project", "backlog", "type", "assigned_to", "created", "changed"]
#
#
#
#
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
    
    try:
        wi_project = response.json()["fields"]["System.TeamProject"] # Mig Factory
    except: 
        wi_project = ""

    try:
        wi_backlog = response.json()["fields"]["System.AreaLevel2"] # AFA
    except: 
        wi_backlog = ""
    wi_type = response.json()["fields"]["System.WorkItemType"] # application, task
    
    # not all the tasks have assigmnment person
    try:
        wi_assignment = response.json()["fields"]["System.AssignedTo"]["displayName"] # mr.david
    except:
        wi_assignment = ""

    wi_created_date = response.json()["fields"]["System.CreatedDate"]
    
    try:
        wi_changed_date = response.json()["fields"]["System.ChangedDate"] # mr.david
    except:
        wi_changed_date = ""

    # working item Relations
    relations = response.json()["relations"]
    for relation in relations: 
        if relation['rel'] == 'System.LinkTypes.Hierarchy-Reverse':
            # print('Parent')
            raw_id = relation['url']
            start_line = raw_id.find('workItems/') + 10
            parent_id = int(raw_id[start_line:])

    new_row = [working_item_id, wi_title, parent_id, wi_state, wi_project, wi_backlog, wi_type, wi_assignment, wi_created_date, wi_changed_date]
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

    # list where ids of children will be stored
    list_of_children = []

    # working item Relations
    try:
        relations = response.json()["relations"]
        for relation in relations: 
            if relation['rel'] == 'System.LinkTypes.Hierarchy-Forward':
                # print('Child')
                raw_id = relation['url']
                start_line = raw_id.find('workItems/') + 10
                child_id = int(raw_id[start_line:])
                list_of_children.append(child_id)
    except:
        list_of_children = []


    
    return list_of_children



# GET ALL APPS
url = "https://dev.azure.com/go-gl-pr-migfactory-axa365/AWS_Migration_Factory/_apis/wit/wiql/90d86a9c-d262-4d01-9e05-102c2d9dc621?api-version=5.1"

headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic '+ authorization
}

response = requests.get(
    url = url,
    headers=headers,
)

# applications is the list(list of dictionaries) of all the applications
applications = response.json()["workItems"]

# n is number of applications
# scrawling one application takes about 25 seconds
n = 10
# first batch
applications = applications[4*n+3:]

# last
# applications = applications[12*n:]


# go through all(n) the apps
for i in range(len(applications)):
    application_id = applications[i]["id"]
    tasks = show_children(application_id)

    # store each application
    df_applications = save_working_item_into_data_frame(application_id, df_applications)

    # go through childs of user_stories (tasks)
    for task in tasks:
        df_applications = save_working_item_into_data_frame(task, df_applications)

    # print(df_applications)

# saves to csv file 
df_applications.to_csv('file_name_43x.csv')

# ok
# 40:41
# 41:42
# 43:

# nok
# 42:43 [4*n+2:4*n+3]
