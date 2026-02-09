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
#Pre-check: Verify AEM is running before stopping



#Application URL 
url=f'https://{aem_base_url}/system/console/status-productinfo.json'
print(f"URL: {url}")
response = requests.get(url, auth=(args.username, args.password))
status_code=response.status_code

#Checking Response Code
if status_code == 200:
   print (f"APP_STATUS= Application up & running- Status Code {status_code} OK")
else:
   raise RuntimeError (f"Application encountered issues: {status_code}") 
   sys.exit(1)



   

