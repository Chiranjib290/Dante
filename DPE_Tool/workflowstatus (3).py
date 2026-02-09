############################START#################################

from datetime import datetime, timedelta
import requests
import json
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed


parser = argparse.ArgumentParser(description='Get Status of Running Workflows ...')
parser.add_argument('username', type=str, help='username')
parser.add_argument('password', type=str, help='Password')

args = parser.parse_args()

with open('infra-reboot-scripts/viewpoint-reboots/scripts/variables/variables.json', 'r') as f:
  data = json.load(f)

aem_base_url=data['aem_base_url']
critical_workflow_model=data['critical model']

# Configuration and Setup
endpoint = "/etc/workflow/instances.json"
url = f"http://{aem_base_url}{endpoint}"

# Fetch Workflow Instances
response = requests.get(url, auth=(args.username, args.password))
if response.status_code == 200:
    workflow_instances = response.json()
else:
    print(f"Failed to fetch workflow instances: {response.status_code}")
    workflow_instances = []
# Function to fetch detailed workflow information

def terminate_workflow(uri):
    try:
        aborted = requests.post(f"http://{aem_base_url}{uri}", data={'state': 'ABORTED'}, auth=(args.username, args.password))
        if not (aborted.status_code >= 200 and aborted.status_code <= 205):
            print(f"Failed to Terminate Workflow for URI {uri}: {aborted.status_code}")
        else:
            print(f"Successfully Terminated Workflow {uri}: {aborted.status_code}")       
    except Exception as e:
        print(f"Request exception for URI {uri}: {e}")

def fetch_workflow_details(uri):
    try:
        detail_response = requests.get(f"http://{aem_base_url}{uri}.json", auth=(args.username, args.password))
        if detail_response.status_code == 200:
            return detail_response.json()
        else:
            print(f"Failed to fetch details for URI {uri}: {detail_response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request exception for URI {uri}: {e}")
        return None

# Process Instances using Threads
running = 0
WORKFLOW_RUNNING = []
WORKFLOW_RUNNING_CRITICAL= []
WORKFLOW_RUNNING_LONG = []

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(fetch_workflow_details, instance['uri']): instance for instance in workflow_instances if 'uri' in instance}
    for future in as_completed(futures):
        instance = futures[future]
        details = future.result()
        if details and details.get('state') == 'RUNNING':
            running += 1
            start_time_str = details.get('startTime')
            start_time = datetime.strptime(start_time_str, "%a %b %d %H:%M:%S %Z %Y")
            duration = datetime.utcnow() - start_time
            WORKFLOW_RUNNING.append(f"Workflow ID - {details['id']} || PAYLOAD - {details['payload']} || MODEL - {details['model']} || DURATION - {duration}")
            if (details['model']).replace("/var/workflow/models/","") in critical_workflow_model:
                WORKFLOW_RUNNING_CRITICAL.append(f"Workflow ID - {details['id']} || PAYLOAD - {details['payload']} || MODEL - {details['model']} || DURATION - {duration}")
            if duration > timedelta(days=30): #check if long running
                #terminate_workflow(details.get('id'))
                WORKFLOW_RUNNING_LONG.append(f"Workflow ID - {details['id']} || PAYLOAD - {details['payload']} || MODEL - {details['model']} || DURATION - {duration}")
            

countOfcriticalworkflowsrunning = len(WORKFLOW_RUNNING_CRITICAL) 
if len(WORKFLOW_RUNNING_CRITICAL) >= 30:
   raise RuntimeError("Too many critical workflows running ...") 
elif len(WORKFLOW_RUNNING_CRITICAL) == 0:
    print (f"WORKFLOWOK=No workflow are running at the moment. Can proceed for reboot ...")   
else:                
    print (f"WORKFLOWOK=Minimum i,e : Only {countOfcriticalworkflowsrunning} critical workflows are running at the moment. Can proceed for reboot ...")                
#Output
print(f"Total RUNNING workflows: {running}")
for workflow in WORKFLOW_RUNNING:
    print(workflow)


print(f"ALL LONG RUNNING workflows:")
for workflow in WORKFLOW_RUNNING_LONG:
    print(workflow)

