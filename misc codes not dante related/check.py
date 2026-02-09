import subprocess
import json

resource_group = 'vmtest_group'
vm_name = 'vmWindows'

# Run the Azure CLI command to get instance view of the VM
result = subprocess.run(
    ["az", "vm", "get-instance-view", "--name", vm_name, "--resource-group", resource_group, "--output", "json"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    vm_info = json.loads(result.stdout)
    power_state = None
    for status in vm_info.get("instanceView", {}).get("statuses", []):
        if status.get("code", "").startswith("PowerState/"):
            power_state = status["code"].split("/")[1]
            break

    if power_state:
        print(f"The VM power state is: {power_state}")
        if power_state.lower() == 'deallocated':
            print("The VM is deallocated.")
        else:
            print("The VM is not deallocated.")
    else:
        print("Unable to determine the power state.")
else:
    print("Error retrieving VM instance view:", result.stderr)
