import requests
from collections import Counter

#aem_base, auth = "https://auth-viewpoint-qa.pwc.com, ('chiranjib.bhattacharyya@pwc.com', 'Change@123456')"
#aem_base, auth = "https://dpe-qa.pwc.com, ('chiranjib.bhattacharyya@pwc.com', 'Change@123456')"
#aem_base, auth = "https://author.hq-stg.pwc.com, ('chiranjib.bhattacharyya@pwc.com', 'Change@123456')
#aem_base, auth = "https://auth-brandsite-qa.pwc.com, ('chiranjib.bhattacharyya@pwc.com', 'Change@123456')
#aem_base, auth = "http://localhost:4502", ('admin', 'admin')
aem_base, auth = "https://auth-customerhub-qa.pwc.com", ('admin', 'PcQ@_3m22')

endpoint = "/etc/workflow/instances.json"
url = aem_base + endpoint
print(f"Fetching workflow instances from: {url}")
state_counter = Counter()
response = requests.get(url, auth=auth)
if response.status_code == 200:
    instances = response.json()
    total_items = len(instances)
    print(f"Found {total_items} workflow instance(s).")
    
    for idx, inst in enumerate(instances, start=1):
        print(f"\nProcessing instance {idx} of {total_items}...")
        uri = inst.get("uri")
        if uri:
            inst_url = aem_base + uri + ".json"
            print(f"Fetching details for: {inst_url}")
            detail_response = requests.get(inst_url, auth=auth)
            if detail_response.status_code == 200:
                details = detail_response.json()
                state = details.get("state", "UNKNOWN").upper()
                state_counter[state] += 1
                print(f"Workflow {details.get('id')} is in state: {state}")
            else:
                print(f"Failed to retrieve details for {uri} (Status Code: {detail_response.status_code})")
        else:
            print(f"No URI found for instance {idx}.")
else:
    print("Error fetching workflow instances.")

for state, count in state_counter.items():
    print(f"{state}: {count} occurrence(s)")