import requests
import json
import re

# Set up authentication and base URL
AUTH = ('chiranjib.bhattacharyya@pwc.com', 'Change@123456')
BASE_URL = "https://auth-viewpoint-qa.pwc.com"

# Endpoints available on the legacy AEM system
ENDPOINTS = {
    "thread_dump": "/system/console/status-threaddump",
    "sling_log": "/system/console/slinglog",
    "bundles": "/system/console/bundles",
    "jmx": "/system/console/jmx",
    "workflow_instances": "/etc/workflow/instances.json"
}

def fetch_endpoint(endpoint: str) -> requests.Response:
    """
    Constructs the full URL for the endpoint and returns the Requests response.
    """
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, auth=AUTH, timeout=30)
        response.raise_for_status()
        return response
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred while fetching {url}: {http_err}")
    except Exception as err:
        print(f"Other error occurred while fetching {url}: {err}")
    return None

def analyze_thread_dump(thread_dump: str):
    """
    Looks for potential stuck threads in the thread dump.
    This simple analysis searches for the word "stuck" or any thread that has been running too long.
    For more advanced processing, you could parse timestamps or specific thread states.
    """
    stuck_keywords = ["stuck", "BLOCKED", "WAITING", "long-running"]
    stuck_lines = []
    for line in thread_dump.splitlines():
        if any(keyword.lower() in line.lower() for keyword in stuck_keywords):
            stuck_lines.append(line.strip())
    if stuck_lines:
        print("Potential stuck thread indications found:")
        for line in stuck_lines:
            print("   ", line)
    else:
        print("No obvious stuck threads detected in the thread dump.")


def analyze_workflow_instances(data):
    """
    Analyzes the JSON from the /etc/workflow/instances.json endpoint.
    Adjusts based on whether data is a list of instances or a dictionary with an "instances" key.
    """
    # Check if the response is a list or a dict containing instances.
    if isinstance(data, list):
        instances = data
    elif isinstance(data, dict):
        instances = data.get("instances", [])
    else:
        print("Unexpected data format from workflow instances endpoint.")
        return

    print(f"Found {len(instances)} workflow instance(s).")
    
    # A simple check: print workflows that have not finished.
    for wf in instances:
        if isinstance(wf, dict):
            status = wf.get("status", "").lower()
            wf_id = wf.get("id", "unknown")
        else:
            # If an instance is unexpectedly not a dict.
            status = ""
            wf_id = "unknown"
        if status not in ["completed", "finished"]:
            print(f"Workflow {wf_id} is still in progress or in an unexpected state (status: {status}).")



def main():
    print("=== Accessing AEM endpoints ===")
    
    # 1. Fetch and analyze thread dump for stuck threads
    print("\nFetching Thread Dump...")
    td_response = fetch_endpoint(ENDPOINTS["thread_dump"])
    if td_response:
        thread_dump = td_response.text
        print("Analyzing thread dump for long running or stuck threads:")
        analyze_thread_dump(thread_dump)
    else:
        print("Failed to retrieve thread dump.")
    
    # 2. Fetch and check workflow instances (jobs)
    print("\nFetching Workflow Instances...")
    wf_response = fetch_endpoint(ENDPOINTS["workflow_instances"])
    if wf_response:
        try:
            workflow_data = wf_response.json()
            analyze_workflow_instances(workflow_data)
        except json.JSONDecodeError as e:
            print("Error decoding JSON from workflow instances endpoint:", e)
    else:
        print("Failed to retrieve workflow instances.")
    
    # 3. Optionally fetch the sling log, bundles and jmx endpoints for additional diagnostics.
    for key in ("sling_log", "bundles", "jmx"):
        print(f"\nFetching {key.replace('_', ' ').title()} Information...")
        response = fetch_endpoint(ENDPOINTS[key])
        if response:
            content = response.text
            # For now, simply outputting the status; for logs you might want to process this data.
            print(f"Successfully fetched {key} information. (Output length: {len(content)} characters)")
        else:
            print(f"Failed to retrieve {key} information.")

if __name__ == "__main__":
    main()
