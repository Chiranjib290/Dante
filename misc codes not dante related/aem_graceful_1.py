#!/usr/bin/env python3
import os
import requests
import subprocess
import time
import json
import sys
import logging
import argparse
import platform

# Configure logging for the script
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def prepare_command(cmd):
    r"""
    Prepares a command string to be executed.

    For Windows, if the command path has spaces and is not already enclosed in double quotes,
    this function encloses the entire command string in double quotes.
    
    Example:
      Input:  C:\Users\cbhattacha015\OneDrive - PwC\Downloads\AEM Learning\Author\crx-quickstart\bin\stop.bat
      Output: "C:\Users\cbhattacha015\OneDrive - PwC\Downloads\AEM Learning\Author\crx-quickstart\bin\stop.bat"
    """
    stripped = cmd.strip()
    if not (stripped.startswith('"') and stripped.endswith('"')):
        return '"' + stripped + '"'
    return stripped


def check_aem_health(url, auth):
    """
    Check if the AEM health endpoint returns HTTP 200.
    The endpoint is typically /system/console/status-productinfo.json.
    """
    try:
        response = requests.get(url, auth=auth, timeout=10)
        if response.status_code == 200:
            logging.info("AEM is healthy at %s", url)
            return True
        else:
            logging.error("AEM health check failed: HTTP %s", response.status_code)
            return False
    except requests.exceptions.RequestException as e:
        logging.error("AEM health check exception: %s", e)
        return False


def check_active_workflows(aem_base_url, auth):
    """
    Optionally check for active workflows using the /bin/workflow.json endpoint.
    If JSON decoding fails (e.g., empty content), log a warning and assume no active workflows.
    """
    #workflow_url = aem_base_url.rstrip('/') + '/bin/workflow.json'
    workflow_url = aem_base_url.rstrip('/') + '/etc/workflow/instances.json'
    
    try:
        response = requests.get(workflow_url, auth=auth, timeout=10)
        try:
            data = response.json()
        except ValueError as e:
            logging.warning("Workflow JSON decode error: %s; assuming no active workflows", e)
            data = {}
        if data:
            logging.warning("Active workflows detected: %s", data)
            return False
        logging.info("No active workflows detected.")
        return True
    except Exception as e:
        logging.error("Exception checking workflows: %s", e)
        return True


def run_command(command):
    """
    Run a given shell command and log its output.
    """
    logging.info("Executing command: %s", command)
    try:
        result = subprocess.run(command,
                                shell=True,
                                check=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        output = result.stdout.decode().strip()
        if output:
            logging.info("Command output: %s", output)
        return 0
    except subprocess.CalledProcessError as e:
        error_output = e.stderr.decode().strip()
        logging.error("Command '%s' failed with error: %s", command, error_output)
        return e.returncode


def stop_aem(stop_cmd):
    """
    Triggers a graceful stop using the provided stop command.
    This method is used for option 1.
    """
    return run_command(stop_cmd)


def kill_aem(aem_base):
    """
    Stops AEM by sending a SIGTERM (kill -15) to the AEM process.
    
    It first attempts to read the process ID from a PID file (assumed location: <AEM_BASE>/quickstart.pid).
    If not found, it uses pgrep to locate the process.
    This method is used for option 2.
    """
    if platform.system() == "Windows":
        logging.error("Option 2 (kill -15) is not supported on Windows")
        return 1

    pid_file = os.path.join(aem_base, "quickstart.pid")
    pid = None
    if os.path.exists(pid_file):
        try:
            with open(pid_file, "r") as f:
                pid = f.read().strip()
        except Exception as e:
            logging.error("Error reading PID file: %s", e)
            return 1
    if not pid:
        # Try to locate the process using pgrep
        try:
            result = subprocess.run("pgrep -f quickstart", shell=True, check=True,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pids = result.stdout.decode().strip().splitlines()
            if pids:
                pid = pids[0]
            else:
                logging.error("No AEM process found via pgrep.")
                return 1
        except Exception as e:
            logging.error("Failed to find AEM process via pgrep: %s", e)
            return 1

    command = f"kill -15 {pid}"
    logging.info("Sending SIGTERM (kill -15) to AEM process with PID %s", pid)
    return run_command(command)


def systemctl_stop():
    """
    Stops AEM via systemctl.
    This method is used for option 3.
    """
    if platform.system() == "Windows":
        logging.error("Option 3 (systemctl) is not supported on Windows")
        return 1
    command = "systemctl stop aem"
    logging.info("Stopping AEM via systemctl")
    return run_command(command)


def start_aem(start_cmd):
    """
    Trigger AEM start using the provided start command.
    """
    return run_command(start_cmd)


def wait_for_shutdown(health_url, auth, max_retries=30, sleep_interval=10):
    """
    Poll the AEM health endpoint until the service is confirmed as shutdown.
    We consider it shutdown when the health check no longer returns HTTP 200.
    """
    logging.info("Waiting for AEM to shutdown...")
    for i in range(max_retries):
        if not check_aem_health(health_url, auth):
            logging.info("AEM appears to be shutdown.")
            return True
        logging.info("AEM still running. Retry %d/%d", i + 1, max_retries)
        time.sleep(sleep_interval)
    return False


def wait_for_startup(health_url, auth, max_retries=30, sleep_interval=10):
    """
    Poll the AEM health endpoint until the service returns HTTP 200.
    """
    logging.info("Waiting for AEM to startup...")
    for i in range(max_retries):
        if check_aem_health(health_url, auth):
            logging.info("AEM is up and running.")
            return True
        logging.info("AEM not up yet. Retry %d/%d", i + 1, max_retries)
        time.sleep(sleep_interval)
    return False


def check_bundles(bundles_url, auth):
    """
    After startup, query the /system/console/bundles.json endpoint.
    This function parses the JSON output and verifies that all bundles are active.
    It expects a "status" key with text like:
      "Bundle information: 591 bundles in total - all 591 active."
    """
    logging.info("Checking bundles status at: %s", bundles_url)
    try:
        response = requests.get(bundles_url, auth=auth, timeout=10)
        if response.ok:
            data = response.json()
            status_text = data.get("status", "").lower()
            logging.info("Bundles status: %s", status_text)
            if "all" in status_text and "active" in status_text:
                logging.info("All bundles are active.")
                return True
            else:
                logging.warning("Not all bundles are active.")
                return False
        else:
            logging.error("Failed to fetch bundles info, HTTP %s", response.status_code)
            return False
    except Exception as e:
        logging.error("Exception during bundles check: %s", e)
        return False


def verify_graceful_shutdown(aem_base_path):
    """
    Verifies that the AEM graceful shutdown was completed successfully.
    Checks include:
      - The error log (located at <AEM_BASE>/logs/error.log) must contain the expected
        "Framework stopped" message.
      - The error log must not contain unwanted keywords such as "corruption", "recovery",
        "oak-run", or "repository recovery".
      - The repository segmentstore directory (<AEM_BASE>/repository/segmentstore) must
        not contain any suspicious items.
    """
    error_log_path = os.path.join(aem_base_path, "logs", "error.log")
    segmentstore_path = os.path.join(aem_base_path, "repository", "segmentstore")
    
    logging.info("Verifying graceful shutdown using error log: %s", error_log_path)
    try:
        with open(error_log_path, "r", encoding="utf-8") as f:
            log_content = f.read()
    except Exception as e:
        logging.error("Failed to open error log at %s: %s", error_log_path, e)
        return False

    if "Framework stopped" not in log_content:
        logging.error("Verification failed: 'Framework stopped' not found in error log.")
        return False

    unwanted_keywords = ["corruption", "recovery", "oak-run", "repository recovery"]
    for keyword in unwanted_keywords:
        if keyword.lower() in log_content.lower():
            logging.error("Verification failed: unwanted keyword '%s' found in error log.", keyword)
            return False

    logging.info("Verifying repository segmentstore at: %s", segmentstore_path)
    try:
        seg_contents = os.listdir(segmentstore_path)
    except Exception as e:
        logging.error("Failed to list repository segmentstore at %s: %s", segmentstore_path, e)
        return False

    for item in seg_contents:
        lower_item = item.lower()
        if "recovery" in lower_item or "corrupt" in lower_item:
            logging.error("Verification failed: found suspicious item '%s' in repository segmentstore.", item)
            return False

    logging.info("Graceful shutdown verified via logs and repository check.")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Perform graceful shutdown and restart of AEM service.")
    parser.add_argument('--aem-url', type=str, default="http://localhost:4502",
                        help="Base URL of the AEM instance (default: http://localhost:4502)")
    # Default stop and start commands (update these paths if needed):
    parser.add_argument('--stop-cmd', type=str,
                        default=r"C:\Users\cbhattacha015\OneDrive - PwC\Downloads\AEM Learning\Author\crx-quickstart\bin\stop.bat",
                        help="Command to gracefully stop AEM")
    parser.add_argument('--start-cmd', type=str,
                        default=r"C:\Users\cbhattacha015\OneDrive - PwC\Downloads\AEM Learning\Author\crx-quickstart\bin\start.bat",
                        help="Command to start AEM")
    parser.add_argument('--username', type=str, default="admin",
                        help="Username for accessing AEM endpoints (default: admin)")
    parser.add_argument('--password', type=str, default="admin",
                        help="Password for accessing AEM endpoints (default: admin)")
    args = parser.parse_args()

    auth = (args.username, args.password)

    logging.info("Starting graceful restart for AEM at: %s", args.aem_url)

    # Define endpoints for health and bundles checks.
    status_endpoint = args.aem_url.rstrip('/') + "/system/console/status-productinfo.json"
    bundles_endpoint = args.aem_url.rstrip('/') + "/system/console/bundles.json"

    # Pre-check: Verify AEM is currently running.
    if not check_aem_health(status_endpoint, auth):
        logging.error("AEM does not appear to be running or accessible; cannot proceed with graceful shutdown.")
        sys.exit(1)

    # Optional: Verify there are no active workflows.
    if not check_active_workflows(args.aem_url, auth):
        logging.error("Active workflows detected; aborting restart to avoid interrupting critical operations.")
        sys.exit(1)

    # Infer AEM base directory from the stop command path.
    # (Assumes the stop command is in <AEM_BASE>/bin/stop.bat)
    aem_base = os.path.dirname(os.path.dirname(args.stop_cmd.strip('"')))
    logging.info("Inferred AEM base directory: %s", aem_base)

    # Prompt the user for the shutdown method.
    print("Select shutdown method:")
    print("1: Stop AEM via stop script")
    print("2: Stop AEM via kill -15 (SIGTERM)")
    print("3: Stop AEM via systemctl stop")
    choice = input("Enter choice (1/2/3): ").strip()

    if choice == "1":
        stop_command = prepare_command(args.stop_cmd)
        ret = stop_aem(stop_command)
    elif choice == "2":
        ret = kill_aem(aem_base)
    elif choice == "3":
        ret = systemctl_stop()
    else:
        logging.error("Invalid shutdown method chosen.")
        sys.exit(1)

    if ret != 0:
        logging.error("AEM stop command failed with exit code %d", ret)
        sys.exit(ret)

    # Wait until AEM shutdown is verified.
    if not wait_for_shutdown(status_endpoint, auth):
        logging.error("AEM did not shutdown gracefully within the expected time.")
        sys.exit(1)
    logging.info("AEM shutdown verified successfully.")

    # Start AEM using the default start command.
    start_command = prepare_command(args.start_cmd)
    ret = start_aem(start_command)
    if ret != 0:
        logging.error("AEM start command failed with exit code %d", ret)
        sys.exit(ret)

    # Wait until AEM startup is confirmed.
    if not wait_for_startup(status_endpoint, auth):
        logging.error("AEM did not startup gracefully within the expected time.")
        sys.exit(1)

    # Verify that the shutdown was graceful by checking logs and repository.
    if not verify_graceful_shutdown(aem_base):
        logging.error("Graceful shutdown verification failed.")
        sys.exit(1)

    logging.info("AEM graceful restart completed successfully!")


if __name__ == "__main__":
    main()
