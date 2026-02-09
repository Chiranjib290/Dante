############################START#################################
 
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
 
 
# #Pre-check: Checking Status of Replication Agents before Reboot
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
      
 
    
for eachAgent in replication_agents:
    QUEUE_STATUS_LIST.append(json.loads(check_replication_queue(eachAgent)))
 
""" for eachAgentStatus in QUEUE_STATUS_LIST:
    if "Queue is not idle" in eachAgentStatus['STATUS']:
         print("############################################")
         print(f"Agent Name: {eachAgentStatus['AGENT_NAME']}")
         print(f"Agent Status: {eachAgentStatus['STATUS']}")
         print(f"Agent Queue: {eachAgentStatus['QUEUE']}")
         agent_name=eachAgentStatus['AGENT_NAME']
         time.sleep(60) #time can be adjusted accordingly
         print("Re-trying Agent Status ... ")
         status=check_replication_queue(agent_name)
         status=(json.loads(status))
         if "Queue is not idle" in status['STATUS']:
             raise RuntimeError(f"FAILED= Replication Agent has stuck jobs. Please validate") 
         else:            
             print("Queue is now clear ...")
             print(f"Agent Name: {eachAgentStatus['AGENT_NAME']}")
             print(f"Agent Status: {eachAgentStatus['STATUS']}")
             print(f"Agent Queue: {eachAgentStatus['QUEUE']}")     
    else:
        print("############################################")
        print(f"Agent Name: {eachAgentStatus['AGENT_NAME']}")
        print(f"Agent Status: {eachAgentStatus['STATUS']}")
        print(f"Agent Queue: {eachAgentStatus['QUEUE']}")  """    
 

def check_agent_status(eachAgentStatus):
   if "Queue is not idle" in eachAgentStatus['STATUS']:
         print("############################################")
         print(f"Agent Name: {eachAgentStatus['AGENT_NAME']}")
         print(f"Agent Status: {eachAgentStatus['STATUS']}")
         print(f"Agent Queue: {eachAgentStatus['QUEUE']}")
         agent_name=eachAgentStatus['AGENT_NAME']
         time.sleep(60) #time can be adjusted accordingly
         print("Re-trying Agent Status ... ")
         status=check_replication_queue(agent_name)
         status=(json.loads(status))
         if "Queue is not idle" in status['STATUS']:
             raise RuntimeError(f"FAILED= Replication Agent has stuck jobs. Please validate") 
         else:            
             print("Queue is now clear ...")
             print(f"Agent Name: {eachAgentStatus['AGENT_NAME']}")
             print(f"Agent Status: {eachAgentStatus['STATUS']}")
             print(f"Agent Queue: {eachAgentStatus['QUEUE']}")     
   else:
        print("############################################")
        print(f"Agent Name: {eachAgentStatus['AGENT_NAME']}")
        print(f"Agent Status: {eachAgentStatus['STATUS']}")
        print(f"Agent Queue: {eachAgentStatus['QUEUE']}") 


for eachAgentStatus in QUEUE_STATUS_LIST:
    check_agent_status(eachAgentStatus)

print(f"REPQUEUE= All Replication Agents are Idle.")
           
 
   