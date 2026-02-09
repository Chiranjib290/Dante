#!/usr/bin/env python3
import requests
import sys
import ipaddress

username = "chiranjib.bhattacharyya@pwc.com"
password = "Change@123456"
auth = (username, password)
aem_base_url = "auth-viewpoint-qa.pwc.com"
replication_agents = ["pwc-ditacontent-replication-agent-jp-pub1"]

try:
    _ = ipaddress.ip_address(aem_base_url)
    protocol = "http"
    port = 4503
    verify_flag = True
except ValueError:
    protocol = "https"
    port = 443
    verify_flag = True

# AEM Status Check
urls = ["/content/pwc/us/en.html",
        "/content/pwc/gx/en.html",
        "/content/pwc/uk/en.html",        
        ]
for url in urls:    
    url = f'{protocol}://{aem_base_url}{url}'
    print(f"URL: {url}")
    response = requests.get(url, auth=auth, verify=verify_flag)
    if response.status_code == 200:
        print(f"APP_STATUS= Application up & running - Status Code {response.status_code} OK")
    else:
        sys.exit(f"Application encountered issues: {response.status_code}")

# Bundles Information and Action
url = f'{protocol}://{aem_base_url}/system/console/bundles.json'
print(f"URL: {url}")
response = requests.get(url, auth=auth, verify=verify_flag)
if response.status_code == 200:
    bundles = response.json()
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

    
else:
    sys.exit("FAILED=Failed to retrieve bundle data")
