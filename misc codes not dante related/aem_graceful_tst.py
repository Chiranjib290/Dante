from pyaem2 import PyAem2
import requests

auth, base = ("admin","admin") , 'http://localhost:4502'
aem = PyAem2(username=auth[0], password=auth[1], host='localhost', port=4502)


url = base + '/system/console/bundles.json'
print(f"URL: {url}")
response = requests.get(url, auth=auth)
status_code = response.status_code

if status_code == 200:
    bundles = response.json()  # parse JSON directly
    status = bundles.get('status', 'Unknown')
    print(f"BUNDLE_STATUS={status}")
    
    active_bundles = [bundle for bundle in bundles.get('data', []) if (bundle.get('state') == 'Active' and bundle.get('fragment') == False)]
    print(f"ACTIVE_STATE_=Total number of bundles with Active State: {len(active_bundles)}")
    
    bundles_toinspect = [bundle for bundle in bundles.get('data', []) if (bundle.get('state') != 'Active' and bundle.get('fragment') == False)]
    print(f"NOT_ACTIVE_STATE=Total number of bundles with not Active State: {len(bundles_toinspect)}")
    
    bundles_fragment = [bundle for bundle in bundles.get('data', []) if bundle.get('fragment') == True]
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
    raise RuntimeError("FAILED=Failed to retrieve bundle data")

for bundle in bundles_toinspect:
    bundle_name = bundle.get("symbolicName")
    try:
        aem.start_bundle(bundle_name)
        print(f"Bundle { bundle_name} has been started successfully.")
    except Exception as e:
        print(f"Failed to start bundle {bundle_name}: {e}")
