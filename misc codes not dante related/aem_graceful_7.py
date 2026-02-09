#!/usr/bin/env python3
import time
import re
import requests

# =====================================================================
# CONFIGURABLE PARAMETERS
# =====================================================================
# The HTTP endpoint for the Sling Log Viewer.
# For a local AEM author instance running on port 4502:
URL = "http://localhost:4502/system/console/slinglog/tailer.txt?name=/logs/error.log"

# Credentials for accessing the endpoint (default for local AEM is often admin/admin)
AUTH = ("admin", "admin")

# The expected number of "Bundle uninstalled" log entries.
EXPECTED_BUNDLE_COUNT = 100

# =====================================================================
# MONITORING FUNCTION
# =====================================================================
def monitor_log():
    """
    Connects to the AEM Sling Log Viewer endpoint and monitors the log stream.
    It counts bundle uninstallation log events, checks for framework stop indication,
    and flags any forced shutdown or unresolved state messages.
    """
    bundle_uninstalled_count = 0
    forced_shutdown_detected = False
    unresolved_states_detected = False
    framework_stopped = False

    # Pre-compiled regular expressions for log markers:
    regex_bundle_uninstalled = re.compile(r"INFO.*OsgiInstallerImpl.*Bundle uninstalled:")
    regex_framework_stopped = re.compile(r"INFO.*Framework Event Dispatcher.*Framework stopped")
    regex_forced_shutdown = re.compile(r"forced shutdown", re.IGNORECASE)
    regex_unresolved = re.compile(r"unresolved", re.IGNORECASE)

    print(f"Connecting to log stream at: {URL}\n")

    try:
        # Connect to the HTTP endpoint with streaming enabled.
        response = requests.get(URL, stream=True, auth=AUTH)
        if response.status_code != 200:
            print("Failed to retrieve log stream. HTTP status code:", response.status_code)
            return

        # Iterate over the streamed lines.
        for line in response.iter_lines(decode_unicode=True):
            # Even with decode_unicode=True, sometimes lines may still be bytes.
            if line:
                if isinstance(line, bytes):
                    line = line.decode("utf-8", errors="replace")
                    
                print(line)  # Optionally, print the log line.
                
                # Check for a bundle uninstallation marker.
                if regex_bundle_uninstalled.search(line):
                    bundle_uninstalled_count += 1
                    print(f"[DEBUG] Bundle uninstalled count: {bundle_uninstalled_count}")

                # Check if framework stopped is logged.
                if regex_framework_stopped.search(line):
                    framework_stopped = True
                    print("[DEBUG] Framework stopped detected.")

                # Flag any forced shutdown alerts.
                if regex_forced_shutdown.search(line):
                    forced_shutdown_detected = True
                    print("[WARNING] Forced shutdown detected!")

                # Flag unresolved states if present.
                if regex_unresolved.search(line):
                    unresolved_states_detected = True
                    print("[WARNING] Unresolved state detected!")

                # When both conditions are met, exit the loop.
                if bundle_uninstalled_count >= EXPECTED_BUNDLE_COUNT and framework_stopped:
                    print("\nAll expected bundles were unregistered and the framework stopped successfully!")
                    break
            else:
                time.sleep(0.5)  # Pause briefly if an empty line is received.
    except KeyboardInterrupt:
        print("\nMonitoring interrupted by user.")
    except Exception as err:
        print("An error occurred while retrieving the log stream:", err)

    # =====================================================================
    # OUTPUT SUMMARY
    # =====================================================================
    print("\nSummary:")
    print(f"Total bundles uninstalled: {bundle_uninstalled_count}")
    if forced_shutdown_detected:
        print("Issue: Forced shutdown detected in logs.")
    if unresolved_states_detected:
        print("Issue: Unresolved states detected in logs.")

# =====================================================================
# MAIN EXECUTION
# =====================================================================
if __name__ == "__main__":
    monitor_log()
