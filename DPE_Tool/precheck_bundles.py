import requests
import json
import argparse
import sys

parser = argparse.ArgumentParser(description='Get Status of Bundles')
parser.add_argument('username', type=str, help='username')
parser.add_argument('password', type=str, help='Password')

args = parser.parse_args()

with open('infra-reboot-scripts/viewpoint-reboots/scripts/variables/variables.json', 'r') as f:
  data = json.load(f)

aem_base_url=data['aem_base_url']

#Pre-check: Checking Status of Bundles before Reboot
url=f'https://{aem_base_url}/system/console/bundles.json'
print(f"URL: {url}")
response = requests.get(url, auth=(args.username, args.password))
status_code=response.status_code
if status_code == 200:
    bundles = json.loads(response.text)
    status = bundles['status']
    print(f"BUNDLE_STATUS={status}")
    active_bundles = [bundle for bundle in bundles['data'] if bundle['state'] == 'Active']
    print(f"ACTIVE_STATE_=Total number of bundles with Active State: {len(active_bundles)}")
    bundles_toinspect=[bundle for bundle in bundles['data'] if bundle['state'] != 'Active']
    print(f"NOT_ACTIVE_STATE=Total number of bundles with not Active State: {len(bundles_toinspect)}")
    ##Check if any bundle has error status
    bundles_error=[bundle for bundle in bundles['data'] if bundle['state'] == 'Installed' or bundle['state'] == 'Resolved' or bundle['state'] == 'Stopping']
    print(f"ERROR_STATE={len(bundles_error)}")
    error_details = [(errorbundle['name'], errorbundle['state']) for errorbundle in bundles_error]
    print(f"ERROR_DETAILS={error_details}")
    details = [(nonactivebundle['name'], nonactivebundle['state']) for nonactivebundle in bundles_toinspect]
    print(f"DETAILS={details}")
else:
    raise RuntimeError("FAILED=Failed to retrieve bundle data") 
    sys.exit(1)  



