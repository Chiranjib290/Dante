from azure.identity import DefaultAzureCredential
from msrest.authentication import BasicTokenAuthentication
from azure.mgmt.compute import ComputeManagementClient

# Your Azure details
subscription_id = 'c3c9c331-d0f7-466e-afd6-107736baf64d'
resource_group = 'vmtest_group'
vm_name = 'vmWindows'

# Obtain an access token using DefaultAzureCredential
credential = DefaultAzureCredential()
token = credential.get_token("https://management.azure.com/.default")

# Wrap the token so that it's compatible with the Azure management client
msrest_credential = BasicTokenAuthentication({"access_token": token.token})

# Create the Compute Management client using the adapted credentials
compute_client = ComputeManagementClient(msrest_credential, subscription_id)

# Retrieve the virtual machine instance view, including its statuses
vm_instance = compute_client.virtual_machines.get(resource_group, vm_name, expand='instanceView')

# Extract the VM's power state from the instance view statuses
power_state = None
for status in vm_instance.instance_view.statuses:
    if status.code.startswith('PowerState/'):
        power_state = status.code.split('/')[1]
        break

if power_state:
    print(f"The VM power state is: {power_state}")
    if power_state.lower() == 'deallocated':
        print("The VM is deallocated.")
    else:
        print("The VM is not deallocated.")
else:
    print("Unable to determine the power state.")
