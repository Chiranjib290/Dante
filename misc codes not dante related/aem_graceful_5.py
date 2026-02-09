import requests
import json
from datetime import datetime, timedelta
import concurrent.futures
from collections import Counter

# Basic Authentication and Base URL
AUTH = ('chiranjib.bhattacharyya@pwc.com', 'Change@123456')
BASE_URL = "https://auth-viewpoint-qa.pwc.com"

# Endpoints for AEM
ENDPOINTS = {
    "thread_dump": "/system/console/status-threaddump",
    "sling_log": "/system/console/slinglog",
    "bundles": "/system/console/bundles",
    "jmx": "/system/console/jmx",
    "workflow_instances": "/etc/workflow/instances.json"
}

def fetch_endpoint(endpoint: str) -> requests.Response:
    """
    Constructs the full URL and returns the Requests response for the given endpoint.
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
    Searches the thread dump output for keywords that indicate stuck or long‐running threads.
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

def fetch_workflow_detail(wf: dict) -> dict:
    """
    For a given workflow instance, check if a 'uri' exists. If so, fetch the detailed
    workflow JSON from BASE_URL + uri + ".json". If not, return the original workflow dict.
    """
    uri = wf.get("uri")
    if uri:
        inst_url = BASE_URL + uri + ".json"
        try:
            response = requests.get(inst_url, auth=AUTH, timeout=30)
            response.raise_for_status()
            detail = response.json()
            return detail
        except Exception as e:
            print(f"Failed to fetch details for URI {uri}: {e}")
            return {}  # Returning an empty dict signals an unsuccessful fetch
    else:
        print(f"No URI found for workflow instance {wf.get('id', 'unknown')}.")
        return wf

def analyze_single_workflow(wf: dict, threshold_minutes: int = 30):
    """
    Analyzes a single detailed workflow. If its state is 'RUNNING', calculates the duration
    from the parsed 'startTime' until now (assumed in UTC). If the elapsed time exceeds the
    threshold (in minutes), returns the workflow (and its duration).
    """
    state = wf.get("state", "").upper()
    if state == "RUNNING":
        start_time_str = wf.get("startTime")
        if not start_time_str:
            print(f"Workflow {wf.get('id', 'unknown')} has no startTime.")
            return None
        try:
            # Parse the startTime; adjust the format string if necessary
            start_time = datetime.strptime(start_time_str, "%a %b %d %H:%M:%S %Z %Y")
        except Exception as e:
            print(f"Error parsing startTime for workflow {wf.get('id', 'unknown')}: {e}")
            return None
        now = datetime.utcnow()
        duration = now - start_time
        if duration > timedelta(minutes=threshold_minutes):
            return wf, duration
    return None

def analyze_workflow_instances(data, threshold_minutes: int = 30):
    """
    Processes the workflow instances data in two parts:
      1. Uses the 'uri' from each instance to fetch detailed information in parallel,
         then counts the actual states.
      2. Analyzes 'RUNNING' workflows concurrently to check if their runtime exceeds
         the specified threshold.
    """
    # Determine where the list of workflows is stored.
    if isinstance(data, list):
        workflows = data
    elif isinstance(data, dict):
        workflows = data.get("instances", [])
    else:
        print("Unexpected data format from workflow instances endpoint.")
        return

    print(f"Found {len(workflows)} workflow instance(s).")

    state_counter = Counter()
    detailed_workflows = []

    # Step 1: Fetch detailed information concurrently using the 'uri' field.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_wf = {executor.submit(fetch_workflow_detail, wf): wf for wf in workflows}
        for future in concurrent.futures.as_completed(future_to_wf):
            detail = future.result()
            if detail:
                detailed_workflows.append(detail)
                state = detail.get("state", "UNKNOWN").upper()
                state_counter[state] += 1
            else:
                state_counter["UNKNOWN"] += 1

    print("\nWorkflow States Summary:")
    for state, count in state_counter.items():
        print(f"  {state}: {count}")

    # Step 2: Analyze RUNNING workflows for long-running execution.
    print(f"\nAnalyzing RUNNING workflows for long-running execution (threshold: {threshold_minutes} minutes)...")
    flagged_workflows = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(analyze_single_workflow, wf, threshold_minutes): wf for wf in detailed_workflows}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:
                flagged_workflows.append(result)

    if flagged_workflows:
        print("\nFlagged long-running workflow(s):")
        for wf, duration in flagged_workflows:
            print(f" - Workflow {wf.get('id', 'unknown')} has been running for {duration} (exceeds {threshold_minutes} minutes).")
    else:
        print("\nNo long-running workflows found.")

def main():
    print("=== Accessing AEM endpoints ===")
    
    # 1. Fetch and analyze thread dump.
    print("\nFetching Thread Dump...")
    td_response = fetch_endpoint(ENDPOINTS["thread_dump"])
    if td_response:
        thread_dump = td_response.text
        print("Analyzing thread dump for long running or stuck threads:")
        analyze_thread_dump(thread_dump)
    else:
        print("Failed to retrieve thread dump.")
    
    # 2. Fetch and analyze workflow instances (including state counter and time-based analysis).
    print("\nFetching Workflow Instances...")
    wf_response = fetch_endpoint(ENDPOINTS["workflow_instances"])
    if wf_response:
        try:
            workflow_data = wf_response.json()
            analyze_workflow_instances(workflow_data, threshold_minutes=30)
        except json.JSONDecodeError as e:
            print("Error decoding JSON from workflow instances endpoint:", e)
    else:
        print("Failed to retrieve workflow instances.")
    
    # 3. Optionally fetch additional endpoints for diagnostics.
    for key in ("sling_log", "bundles", "jmx"):
        print(f"\nFetching {key.replace('_', ' ').title()} Information...")
        response = fetch_endpoint(ENDPOINTS[key])
        if response:
            content = response.text
            print(f"Successfully fetched {key} information. (Output length: {len(content)} characters)")
        else:
            print(f"Failed to retrieve {key} information.")

if __name__ == "__main__":
    main()

""" 
                

                #post_resp = requests.post(inbox_url , data=post_data, auth=(self.user, self.passwd),timeout=self.timeout)
                
                #status_code = 201
                self.logger.debug('Executed : ' + str(uri) +
                                ' - \n'+str(aborted.text))
                msg = str(uri) + "   :   "

                if status_code >= 200 and status_code <= 205:
                    msg = msg + "Processed("+str(status_code)+")"
                elif(status_code == 401):
                    msg = "Wrong username and Password - Http status " + \
                        str(status_code)
                else:
                    msg = msg + "Failed("+str(status_code)+")"
                self.logger.info("Terminate Workflow: Payload: " +
                                str(uri) + " - Status Code: " + str(status_code))
            elif(status_code == 401):
                msg = "Wrong username and Password - Http status " + \
                        str(status_code)
            else:
                msg = "Some Error occured while connecting. Http Status "+ \
                        str(status_code)

            return msg """