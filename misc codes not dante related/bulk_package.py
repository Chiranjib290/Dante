import requests
from requests.auth import HTTPBasicAuth
import json
import time
 
AEM_HOST = "http://localhost:4502"
USERNAME = "admin"
PASSWORD = "admin"
 
GROUP = "custom"
PACKAGE_NAME = "users-package"
PACKAGE_PATH = f"/etc/packages/{GROUP}/{PACKAGE_NAME}"
 
# User paths you want as filters
USER_PATHS = [
    "/home/users/s/sBauoSaZdCZsY1imKwTT",
    "/home/users/3/3SezB0f4_c1iPz-eXNVq",
    "/home/users/Z/Z_YO37tQfEG-Lwopfrcj",
    "/home/users/U/Uaaj3GiJjQCW4Io6rix-",
    "/home/users/I/IlnUwNhzTOaSA12yHTw0"
]
 
auth = HTTPBasicAuth(USERNAME, PASSWORD)
 
 
def create_package():
    url = f"{AEM_HOST}/crx/packmgr/service/.json"
    data = {
        "cmd": "create",
        "group": GROUP,
        "name": PACKAGE_NAME,
        "packageName": PACKAGE_NAME,
        "version": "1.0"
    }
    print("Creating package...")
    resp = requests.post(url, data=data, auth=auth)
    if resp.status_code == 200:
        print("Package created.")
        return True
    else:
        print(f"Failed to create package: {resp.status_code} {resp.text}")
        return False
 
 
def update_filters():
    # Filters are stored at:
    # /etc/packages/<group>/<packageName>/jcr:content/filters
    # We update filters with paths from USER_PATHS
 
    url = f"{AEM_HOST}{PACKAGE_PATH}/jcr:content.filters.json"
    print("Updating filters...")
 
    # Construct filters JSON
    filters = {"jcr:primaryType": "sling:OrderedFolder"}
 
    # Each filter is an ordered node: "1", "2", "3", etc.
    for idx, path in enumerate(USER_PATHS, 1):
        filters[str(idx)] = {
            "jcr:primaryType": "cq:PackageFilter",
            "root": path
        }
 
    headers = {'Content-Type': 'application/json'}
 
    resp = requests.post(url, data=json.dumps(filters), headers=headers, auth=auth)
    if resp.status_code in (200, 201):
        print("Filters updated.")
        return True
    else:
        print(f"Failed to update filters: {resp.status_code} {resp.text}")
        return False
 
 
def build_package():
    url = f"{AEM_HOST}/crx/packmgr/service/.json"
    data = {
        "cmd": "build",
        "path": PACKAGE_PATH
    }
    print("Building package...")
    resp = requests.post(url, data=data, auth=auth)
    if resp.status_code == 200:
        print("Package built successfully.")
        return True
    else:
        print(f"Failed to build package: {resp.status_code} {resp.text}")
        return False
 
 
def install_package():
    url = f"{AEM_HOST}/crx/packmgr/service/.json"
    data = {
        "cmd": "install",
        "path": PACKAGE_PATH
    }
    print("Installing package...")
    resp = requests.post(url, data=data, auth=auth)
    if resp.status_code == 200:
        print("Package installed successfully.")
        return True
    else:
        print(f"Failed to install package: {resp.status_code} {resp.text}")
        return False
 
 
if __name__ == "__main__":
    if create_package():
        time.sleep(1)  # small delay for JCR changes to propagate
        if update_filters():
            time.sleep(1)
            if build_package():
                time.sleep(1)
                install_package()