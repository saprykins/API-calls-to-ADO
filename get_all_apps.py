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
print(response.json()["workItems"][0]["id"])




# GET TITLE, PARENT, CHILD ETC. FOR EACH APP
url = 'https://dev.azure.com/go-gl-pr-migfactory-axa365/_apis/wit/workItems/3051?$expand=all'

headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic '+authorization
}

response = requests.get(
    url = url,
    headers=headers,
)

print(response.text)
