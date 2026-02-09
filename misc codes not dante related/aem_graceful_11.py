import requests

# URL for retrieving bundles from the AEM instance
bundles_url = "http://localhost:4502/system/console/bundles.json"
# Replace these credentials if your AEM instance uses different ones
auth_credentials = ('admin', 'admin')

# Make a GET request to retrieve the bundles in JSON format
response = requests.get(bundles_url, auth=auth_credentials)
ls = []
if response.status_code == 200:
    bundles_data = response.json()
    # The JSON response contains a 'data' key with a list of bundle details
    bundles = bundles_data.get('data', [])
    
    # Print each bundle with its id, name, and state
    print("Installed Bundles:")
    for bundle in bundles:
        bundle_id = bundle.get('id', 'N/A')
        bundle_name = bundle.get('name', 'N/A')
        bundle_state = bundle.get('state', 'N/A')
        print(f"{bundle_id} - {bundle_name} ({bundle_state})")
        ls.append(bundle_name)
    
    # Display the total count of installed bundles
    print("\nTotal number of bundles:", len(bundles))
else:
    print("Failed to retrieve bundle information. Status code:", response.status_code)


for x in ls: print(x)