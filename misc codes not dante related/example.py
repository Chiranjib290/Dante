import requests
import json
import argparse
import sys
import os
 
parser = argparse.ArgumentParser(description='Get Status of Bundles')
parser.add_argument('username', type=str, help='username')
parser.add_argument('password', type=str, help='Password')
parser.add_argument('variable', type=str, help='variable filename')
 
 
 
 
args = parser.parse_args()
 
filename = args.variable 
base_path = "infra-reboot-scripts/viewpoint-reboots/scripts/variables"
full_path = os.path.join(base_path, filename)
 
with open(full_path, 'r') as f:
  data = json.load(f)
 
aem_base_url=data['aem_base_url']
#Pre-check: Verify AEM is running before stopping

# username = "chiranjib.bhattacharyya@in.pwc.com"
# password = "Change@123456" 
# aem_base_url = "madison-dev.pwc.com"


def status_check(url, ignore_auth=False):
    if ignore_auth:
        response = requests.get(url)
    else:    
        #response = requests.get(url, auth=(username, password))
        response = requests.get(url, auth=(args.username, args.password))
    status_code=response.status_code
    if status_code == 200:
        print (f"APP_STATUS= Application up & running- Status Code {status_code} OK")
        print (f"APP_STATUS_CODE={status_code}")
    else:
        print (f"Application encountered issues: {status_code}") 
        print (f"APP_STATUS_CODE={status_code}")
        #sys.exit(1)    
    return status_code

#Application URL 
url=f'http://{aem_base_url}/system/console/status-productinfo.json'
url2=f'http://{aem_base_url}'

print(f"URL: {url}")

if status_check(url)!=200:
    print(f"URL: {url2}")
    status_check(url2,True)

#Checking Response Code
