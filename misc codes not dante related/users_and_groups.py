import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from typing import Dict, List, Optional

BASE_URL = "http://localhost:4502"
BASE_URL = "https://auth-viewpoint.pwc.com"
AUTH = ("chiranjib.bhattacharyya@pwc.com", "Change@123456")  # hardcoded credentials

MEMBERS: Dict[str, List[str]] = {}

def _multipart_fields(mapping: dict) -> dict:
    return {k: (None, str(v)) for k, v in mapping.items()}

def create_user(user_id: str, first_name: str, last_name: str, password: str = "admin") -> requests.Response:
    url = f"{BASE_URL.rstrip('/')}/libs/granite/security/post/authorizables"
    fields = {
        "createUser": user_id,
        "authorizableId": user_id,
        "rep:password": password,
        "profile/givenName": first_name,
        "profile/familyName": last_name
    }
    return requests.post(url, auth=HTTPBasicAuth(*AUTH), files=_multipart_fields(fields), timeout=30)

def load_group_members(group_path: str, timeout: int = 30) -> Optional[List[str]]:

    # Return cached value if present
    if group_path in MEMBERS:
        return MEMBERS[group_path]

    # Validate and normalize group_path
    if not group_path:
        print(f"load_group_members: empty group_path for '{group_path}'")
        return None

    base = BASE_URL.rstrip('/')
    if not group_path.startswith('/'):
        group_path = '/' + group_path
    url = f"{base}{group_path}.json"

    try:
        resp = requests.get(url, auth=HTTPBasicAuth(*AUTH), timeout=timeout)
    except Exception as e:
        print(f"Failed to fetch group '{group_path}' at '{url}': {e}")
        return None

    if resp.status_code != 200:
        print(f"Unexpected HTTP {resp.status_code} when fetching group '{group_path}' at '{url}'")
        return None

    try:
        payload = resp.json()
    except ValueError:
        print(f"Invalid JSON returned for group '{group_path}' at '{url}'")
        return None

    members = payload.get("rep:members")
    if members is None:
        members_list: List[str] = []
    elif isinstance(members, list):
        members_list = [str(m) for m in members]
    else:
        members_list = [str(members)]

    # Cache the members list
    MEMBERS[group_path] = members_list
    return members_list


def remove_user_from_group_by_userid(user_id: str, group_path: str) -> bool:
    if not group_path:
        print("empty group_path")
        return False
    key = group_path if group_path.startswith("/") else "/" + group_path
    # Ensure group members are loaded (cache)
    members = load_group_members(key)
    print(f"{key} - {members}")
    if members is None:
        print(f"Members List is empty for group_path - {group_path}")
        return None

    # Resolve user path if necessary
    uri = f"{BASE_URL}/bin/querybuilder.json?1_property=rep%3aauthorizableId&1_property.value={user_id}&p.hits=selective&p.properties=jcr%3apath%20rep%3aauthorizableId%20jcr%3auuid&path=%2fhome%2fusers%2f&type=rep%3aUser"
    try:
        resp = requests.get(uri, auth=HTTPBasicAuth(*AUTH), timeout=30)
    except Exception as e:
        print(f"Failed to fetch User '{user_id}' at '{uri}': {e}")
        return None

    if resp.status_code != 200:
        print(f"Unexpected HTTP {resp.status_code} when fetching user '{user_id}' at '{uri}'")
        return None

    try:
        payload = resp.json()
    except ValueError:
        print(f"Invalid JSON returned for group '{user_id}' at '{uri}'")
        return None

    user_details = payload.get("hits")
    if user_details !=[]:
        user=user_details[0]
        au_id = user.get("rep:authorizableId")
        uuid = user.get("jcr:uuid")
    print(uuid)
    # Check membership using both uuid and authorizableId
    if not(uuid in members):
        print(f"User '{au_id}' (uuid: {uuid}) not in group '{key}'")
        return None

    # POST to group .rw.html with addMember
    url = f"{BASE_URL.rstrip('/')}{key}.rw.html"
    data = {"removeMembers": au_id}
    try:
        resp = requests.post(url, data=data, auth=HTTPBasicAuth(*AUTH), timeout=30)
    except Exception as e:
        print(f"Failed to remove user '{au_id}' to group '{key}': {e}")
        return False

    if resp.status_code in (200, 201):
        members.remove(uuid)
        print(f"{key} - {members}")
        print(f"Removed user '{au_id}' (uuid: {uuid}) from group '{key}'")
        return True
    else:
        print(f"Failed to remove user '{au_id}' from group '{key}': HTTP {resp.status_code} {resp.text}")
        return False


def add_user_to_group_by_userid(user_id: str, group_path: str) -> bool:
    if not group_path:
        print("add_user_to_group_by_userid: empty group_path")
        return False
    key = group_path if group_path.startswith("/") else "/" + group_path
    # Ensure group members are loaded (cache)
    members = load_group_members(key)

    if members is None:
        # initialize empty list so we can still attempt add
        MEMBERS.setdefault(key, [])
        members = MEMBERS[key]
        
    print(f"{key} - {members}")

    # Resolve user path if necessary
    uri = f"{BASE_URL}/bin/querybuilder.json?1_property=rep%3aauthorizableId&1_property.value={user_id}&p.hits=selective&p.properties=jcr%3apath%20rep%3aauthorizableId%20jcr%3auuid&path=%2fhome%2fusers%2f&type=rep%3aUser"
    try:
        resp = requests.get(uri, auth=HTTPBasicAuth(*AUTH), timeout=30)
    except Exception as e:
        print(f"Failed to fetch User '{user_id}' at '{uri}': {e}")
        return None

    if resp.status_code != 200:
        print(f"Unexpected HTTP {resp.status_code} when fetching user '{user_id}' at '{uri}'")
        return None

    try:
        payload = resp.json()
    except ValueError:
        print(f"Invalid JSON returned for group '{user_id}' at '{uri}'")
        return None

    user_details = payload.get("hits")
    if user_details !=[]:
        user=user_details[0]
        au_id = user.get("rep:authorizableId")
        uuid = user.get("jcr:uuid")
        user_path = user.get("jcr:path")

    # Check membership using both uuid and authorizableId
    if uuid in members:
        print(f"User '{au_id}' (uuid: {uuid}) already in group '{key}'")
        return True

    # POST to group .rw.html with addMember
    url = f"{BASE_URL.rstrip('/')}{key}.rw.html"
    data = {"addMembers": au_id}
    #data = {"removeMembers": au_id}
    try:
        resp = requests.post(url, data=data, auth=HTTPBasicAuth(*AUTH), timeout=30)
    except Exception as e:
        print(f"Failed to add user '{au_id}' to group '{key}': {e}")
        return False

    if resp.status_code in (200, 201):
        members.append(uuid)
        print(f"Added user '{au_id}' (uuid: {uuid}) to group '{key}'")
        print(f"{key} - {members}")
        return True
    else:
        print(f"Failed to add user '{au_id}' to group '{key}': HTTP {resp.status_code} {resp.text}")
        return False

def read_and_create_from_excel_by_position(path: str = "test.xlsx"):

    df = pd.read_excel(path, dtype=str, header=0).fillna("")

    if df.shape[1] < 3:
        raise ValueError("Excel must have at least three columns for email_id, first name and last name")

    for idx in range(len(df)):
        row = df.iloc[idx]
        user_id = str(row.iloc[0]).strip()
        first_name = str(row.iloc[1]).strip() if df.shape[1] > 1 else ""
        last_name = str(row.iloc[2]).strip() if df.shape[1] > 2 else ""
        groups_cell = str(row.iloc[3]).strip() if df.shape[1] > 3 else ""

        # Parse groups into a list, splitting on commas and stripping whitespace
        groups = [g.strip() for g in groups_cell.split(",") if g.strip()] if groups_cell else []
        for grouppath in groups:
            load_group_members(grouppath)
        # groups list is created but not acted upon here
        print(f"[{idx}] Creating user '{user_id}' (givenName='{first_name}', familyName='{last_name}'), groups parsed: {groups}")

        try:
            resp = create_user(user_id, first_name, last_name)
            print(f"[{idx}] HTTP {resp.status_code}")
        except Exception as e:
            print(f"[{idx}] Exception while creating user '{user_id}': {e}")
            continue

        # After creating the user, attempt to add to each group (groups are repository paths)
        for grouppath in groups:
            # Attempt add only if grouppath is non-empty
            if not grouppath:
                continue
            added = add_user_to_group_by_userid(user_id, grouppath)
            print(f"[{idx}] add to '{grouppath}': {added}")


def read_and_remove_from_excel_by_position(path: str = "test.xlsx"):

    df = pd.read_excel(path, dtype=str, header=0).fillna("")

    if df.shape[1] < 3:
        raise ValueError("Excel must have at least three columns for email_id, first name and last name")

    for idx in range(len(df)):
        row = df.iloc[idx]
        user_id = str(row.iloc[0]).strip()
        first_name = str(row.iloc[1]).strip() if df.shape[1] > 1 else ""
        last_name = str(row.iloc[2]).strip() if df.shape[1] > 2 else ""
        groups_cell = str(row.iloc[3]).strip() if df.shape[1] > 3 else ""

        # Parse groups into a list, splitting on commas and stripping whitespace
        groups = [g.strip() for g in groups_cell.split(",") if g.strip()] if groups_cell else []
        for grouppath in groups:
            load_group_members(grouppath)
        # groups list is created but not acted upon here
        print(f"[{idx}] Removing user '{user_id}' (givenName='{first_name}', familyName='{last_name}'), groups parsed: {groups}")

        # After creating the user, attempt to add to each group (groups are repository paths)
        for grouppath in groups:
            # Attempt add only if grouppath is non-empty
            if not grouppath:
                continue
            removed = remove_user_from_group_by_userid(user_id, grouppath)
            print(f"[{idx}] Remove {user_id} from '{grouppath}': {removed}")


if __name__ == "__main__":

    #read_and_create_from_excel_by_position("test.xlsx")
    read_and_remove_from_excel_by_position("test.xlsx")