import requests
import json
import argparse
import time
import sys

parser = argparse.ArgumentParser(description='Get Status of Replication Queue')
parser.add_argument('username', type=str, help='username')
parser.add_argument('password', type=str, help='Password')

args = parser.parse_args()

with open('infra-reboot-scripts/viewpoint-reboots/scripts/variables/variables.json', 'r') as f:
  data = json.load(f)

aem_base_url=data['aem_base_url']
replication_agents=data['replication_agents']

QUEUE_STATUS_LIST=[]


##Pre-check: Checking Status of Replication Agents before Reboot
def check_replication_queue(agent):
  url=f'https://{aem_base_url}/etc/replication/agents.author/{agent}/jcr:content.json'
  response = requests.get(url, auth=(args.username, args.password))
  if response.status_code == 200:
     replication_agent=json.loads(response.text)
     isEnabled = replication_agent.get('enabled', "false")
     if isEnabled == 'true':
       url=f'https://{aem_base_url}/etc/replication/agents.author/{agent}/jcr:content.queue.json'
       response = requests.get(url, auth=(args.username, args.password))
       replicationStatusjson = json.loads(response.text)
       replicationStatus = replicationStatusjson['queue']
       if not replicationStatus:
            response = {
            "AGENT_NAME": agent,
            "STATUS": "Queue is idle",
            "QUEUE": replicationStatus
            }
            return json.dumps(response)            
       else:
            response = {
            "AGENT_NAME": agent,
            "STATUS": "Queue is not idle. Please find the details.",
            "QUEUE": replicationStatus
            }
    
            return json.dumps(response)
     else:
        response = {
            "AGENT_NAME": agent,
            "STATUS": "Agent is not enabled.",
            "QUEUE": "Not Available"
            }   
        return json.dumps(response)
  else:
      raise RuntimeError("Failed to retrieve Replication Agent data") 
      sys.exit(1)

      
def VerifyAgentStatus(agent_name):
    status=check_replication_queue(agent_name)
    status=(json.loads(status))     
    if "Queue is not idle" in status['STATUS']:
        return (f"{agent_name}") 
    else:            
        return(f"OK : Agent Name: {agent_name}")
    
for eachAgent in replication_agents:
    QUEUE_STATUS_LIST.append(json.loads(check_replication_queue(eachAgent)))

for eachAgentStatus in QUEUE_STATUS_LIST:
    print(f"Agent Name: {eachAgentStatus['AGENT_NAME']}")
    print(f"Agent Status: {eachAgentStatus['STATUS']}")
    print(f"Agent Queue: {eachAgentStatus['QUEUE']}")  

for eachAgentStatus in QUEUE_STATUS_LIST:
    agent_name=eachAgentStatus['AGENT_NAME']
    VerifyeachAgentStatus=VerifyAgentStatus(agent_name)
    if "OK" in VerifyeachAgentStatus:
        print(VerifyeachAgentStatus)
    else:
        print(f"{VerifyeachAgentStatus} - Retrying Agent Status ... ")    
        time.sleep(90)
        VerifyeachfailedAgentStatus=VerifyAgentStatus(VerifyeachAgentStatus)
        if "OK" in VerifyeachfailedAgentStatus:
          print(VerifyeachfailedAgentStatus)
        else:
           print(f"{VerifyeachfailedAgentStatus} - Retrying Agent Status for the second time ... ")    
           time.sleep(90)
           VerifyeachFailedfailedAgentStatus=VerifyAgentStatus(VerifyeachfailedAgentStatus)
           if "OK" in VerifyeachFailedfailedAgentStatus:
             print(VerifyeachFailedfailedAgentStatus)
           else:
              raise RuntimeError( "Replication Agent has stuck jobs. Please validate")          
              sys.exit(1)

print(f"REPQUEUE= All Replication Agents are Idle.")


           

   

         
    
        
    