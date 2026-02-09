import requests
import json
import argparse
import sys
import time
import ipaddress
from pyaem2 import PyAem2

parser = argparse.ArgumentParser(description='Get Status of Bundles')
parser.add_argument('username', type=str, help='username')
parser.add_argument('password', type=str, help='Password')
args = parser.parse_args()

with open('infra-reboot-scripts/viewpoint-reboots/scripts/variables/variables.json', 'r') as f:
    data = json.load(f)

aem_base_url = data['aem_base_url']
replication_agents = data['replication_agents']
auth = (args.username, args.password)
QUEUE_STATUS_LIST = []

# Check if aem_base_url is an IP address. 
# If it is an IP, use http (port 4502); otherwise, use https (port 443).
try:
    _ = ipaddress.ip_address(aem_base_url)
    protocol = "http"
    port = 4502
    # When using http, SSL certificate verification is irrelevant.
    verify_flag = True
except ValueError:
    protocol = "https"
    port = 443
    verify_flag = True

# 1. Response Code
url = f'{protocol}://{aem_base_url}/system/console/status-productinfo.json'
print(f"URL: {url}")
response = requests.get(url, auth=auth, verify=verify_flag)
status_code = response.status_code
if status_code == 200:
    print(f"APP_STATUS= Application up & running - Status Code {status_code} OK")
else:
    raise print(f"Application encountered issues: {status_code}")
    sys.exit(1)

# 2. Replication Queue
def check_replication_queue(agent):
    url = f'{protocol}//{aem_base_url}/etc/replication/agents.author/{agent}/jcr:content.json'
    response = requests.get(url, auth=auth, verify=verify_flag)
    if response.status_code == 200:
        replication_agent = response.json()
        is_enabled = replication_agent.get('enabled', "false")
        return is_enabled == 'true'
    else:
        raise print("Failed to retrieve Replication Agent data")

disabled_agents = []

# Check each replication agent and print the status
for agent in replication_agents:
    agent_status = check_replication_queue(agent)
    if not agent_status:
        disabled_agents.append(agent)
    
if disabled_agents:
    print("Disabled Agents are : ")
    for agnt in disabled_agents:
        print(agnt)
else:
    print("All agents are enabled\n\n")

# 3. Bundles (Active and Else)
url = f'{protocol}://{aem_base_url}/system/console/bundles.json'
print(f"URL: {url}")
response = requests.get(url, auth=auth, verify=verify_flag)
status_code = response.status_code
if status_code == 200:
    bundles = response.json()  # parse JSON directly
    status = bundles.get('status', 'Unknown')
    print(f"BUNDLE_STATUS={status}")
    
    active_bundles = [bundle for bundle in bundles.get('data', []) 
                      if (bundle.get('state') == 'Active' and bundle.get('fragment') == False)]
    print(f"ACTIVE_STATE_=Total number of bundles with Active State: {len(active_bundles)}")
    
    bundles_toinspect = [bundle for bundle in bundles.get('data', []) 
                           if (bundle.get('state') != 'Active' and bundle.get('fragment') == False)]
    print(f"NOT_ACTIVE_STATE=Total number of bundles with not Active State: {len(bundles_toinspect)}")
    
    bundles_fragment = [bundle for bundle in bundles.get('data', []) 
                          if bundle.get('fragment') == True]
    print(f"FRAGMENT_STATE=Total number of bundles with Fragment State: {len(bundles_fragment)}")

    # Check if any bundle has error status
    bundles_error = [bundle for bundle in bundles.get('data', []) 
                       if bundle.get('state') in ['Installed', 'Resolved', 'Stopping', 'Starting']]
    print(f"ERROR_STATE={len(bundles_error)}")
    
    error_details = [(errorbundle.get('name'), errorbundle.get('state')) for errorbundle in bundles_error]
    print(f"ERROR_DETAILS={error_details}")
    
    details = [(nonactivebundle.get('name'), nonactivebundle.get('state')) for nonactivebundle in bundles_toinspect]
    print(f"DETAILS={details}")

    # Instantiate PyAem2 with consistent parameters.
    aem = PyAem2(username=auth[0], password=auth[1], host=aem_base_url, port=port, protocol=protocol)
    for bundle in bundles_toinspect:
        bundle_name = bundle.get("symbolicName")
        try:
            aem.start_bundle(bundle_name)
            print(f"Bundle {bundle_name} has been started successfully.")
        except Exception as e:
            print(f"Failed to start bundle {bundle_name}: {e}")
else:
    raise print("FAILED=Failed to retrieve bundle data")
    sys.exit(1)
