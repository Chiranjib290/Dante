import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

#BASE_URL,AUTH = "http://localhost:4502", ("admin","admin")
BASE_URL,AUTH = "https://auth-viewpoint.pwc.com", ("chiranjib.bhattacharyya@pwc.com", "Change@123456")
#BASE_URL,AUTH = "https://dpe.pwc.com", ("chiranjib.bhattacharyya@in.pwc.com", "Change@123456")


MEMBERS = {}
USERS = {}

BASE_URL=BASE_URL.rstrip('/')
TIMEOUT = 30
def _multipart_fields(mapping: dict) -> dict:
    return {k: (None, str(v)) for k, v in mapping.items()}

def create_user(user_id: str, first_name: str, last_name: str, password: str = "admin") -> requests.Response:
    url = f"{BASE_URL}/libs/granite/security/post/authorizables"
    fields = {
        "createUser": user_id,
        "authorizableId": user_id,
        "rep:password": password,
        "profile/givenName": first_name,
        "profile/familyName": last_name
    }
    return requests.post(url, auth=HTTPBasicAuth(*AUTH), files=_multipart_fields(fields), timeout=TIMEOUT)


def groups_having_id(replicate_id):
    groups = []
    url = f"{BASE_URL}/bin/querybuilder.json?1_property=rep%3amembers&1_property.operation=like&1_property.value=%25{load_uuid(replicate_id)}%25&p.hits=selective&p.limit=-1&p.properties=jcr%3apath%20rep%3aauthorizableId%20rep%3amembers&path=%2fhome%2fgroups%2f&type=rep%3aGroup"
    try:
        resp = requests.post(url, auth=HTTPBasicAuth(*AUTH), timeout=TIMEOUT)
    except Exception as e:
        print(f"Failed to fetch Groups for user '{replicate_id}' at '{url}': {e}")
        return None

    if resp.status_code != 200:
        print(f"Unexpected HTTP {resp.status_code} when fetching groups for user '{replicate_id}' at '{url}'")
        return None

    try:
        payload = resp.json()
    except ValueError:
        print(f"Invalid JSON returned for user '{replicate_id}' at '{url}'")
        return None

    group_details = payload.get("hits")
    if group_details !=[]:
        for group in group_details:
            group_path=group.get("jcr:path")
            group_id=group.get("rep:authorizableId")
            members=group.get("rep:members")
            groups.append(group_id)
            if group_id not in MEMBERS:
                if members is None:
                    members_list = []
                elif isinstance(members, list):
                    members_list = [str(m) for m in members]
                else:
                    members_list = [str(members)]
                MEMBERS[group_id]={"path":group_path, "members": members_list}
        return groups
    print(f"No groups for the user - {replicate_id}")
    return None

def load_uuid(user_id):
    if user_id in USERS:
        return USERS[user_id]

    if not user_id:
        print(f"load_users: empty user_id for '{user_id}'")
        return None

    uri = f"{BASE_URL}/bin/querybuilder.json?1_property=rep%3aauthorizableId&1_property.value={user_id}&p.hits=selective&p.properties=jcr%3apath%20rep%3aauthorizableId%20jcr%3auuid&path=%2fhome%2fusers%2f&type=rep%3aUser"
    try:
        resp = requests.get(uri, auth=HTTPBasicAuth(*AUTH), timeout=TIMEOUT)
    except Exception as e:
        print(f"Failed to fetch User '{user_id}' at '{uri}': {e}")
        return None

    if resp.status_code != 200:
        print(f"Unexpected HTTP {resp.status_code} when fetching user '{user_id}' at '{uri}'")
        return None

    try:
        payload = resp.json()
    except ValueError:
        print(f"Invalid JSON returned for user '{user_id}' at '{uri}'")
        return None

    user_details = payload.get("hits")
    if user_details !=[]:
        user=user_details[0]
        uuid = user.get("jcr:uuid")
        USERS[user_id] = uuid
        return uuid
    print(f"No such user exists : user_id - {user_id}")
    return None

def load_group_members(group_id: str):
    if group_id in MEMBERS:
        return MEMBERS[group_id]

    if not group_id:
        print(f"load_group_members: empty group_id for '{group_id}'")
        return None

    uri=f"{BASE_URL}/bin/querybuilder.json?1_property=rep%3aauthorizableId&1_property.value={group_id}&p.hits=selective&p.properties=jcr%3apath%20rep%3amembers&path=%2fhome%2fgroups%2f&type=rep%3aGroup"
    try:
        resp = requests.get(uri, auth=HTTPBasicAuth(*AUTH), timeout=TIMEOUT)
    except Exception as e:
        print(f"Failed to fetch Group '{group_id}' at '{uri}': {e}")
        return None

    if resp.status_code != 200:
        print(f"Unexpected HTTP {resp.status_code} when fetching Group '{group_id}' at '{uri}'")
        return None

    try:
        payload = resp.json()
    except ValueError:
        print(f"Invalid JSON returned for group '{group_id}' at '{uri}'")
        return None

    group_details = payload.get("hits")
    if group_details ==[]:
        print(f"No Group with group id - {group_id} exists")
        return None
    else:
        group=group_details[0]
        members = group.get("rep:members")
        group_path = group.get("jcr:path")
        if members is None:
            members_list = []
        elif isinstance(members, list):
            members_list = [str(m) for m in members]
        else:
            members_list = [str(members)]

        MEMBERS[group_id] = {"path":group_path, "members": members_list}
        return MEMBERS[group_id]

   


def remove_user_from_group_by_userid(user_id: str, group_id: str) -> bool:
    if not group_id:
        print("empty group_id")
        return False
    group_details = load_group_members(group_id)
    members = group_details["members"]
    group_path = group_details["path"]
    #print(f"{group_id} - {members}")
        
    if not group_path:
        print(f"None path for group - {group_id}")
        return False
    if members is None or members == []:
        print(f"Members List is empty for group_id - {group_id}")
        return None

    uuid = load_uuid(user_id)
    #print(uuid)
    if not(uuid in members):
        print(f"User '{user_id}' (uuid: {uuid}) not in group '{group_id}'")
        return None

    url = f"{BASE_URL}{group_path}.rw.html"
    data = {"removeMembers": user_id}
    try:
        resp = requests.post(url, data=data, auth=HTTPBasicAuth(*AUTH), timeout=TIMEOUT)
    except Exception as e:
        print(f"Failed to remove user '{user_id}' to group '{group_id}': {e}")
        return False

    if resp.status_code in (200, 201):
        members.remove(uuid)
        #print(f"{group_id} - {members}")
        print(f"Removed user '{user_id}' (uuid: {uuid}) from group '{group_id}'")
        return True
    else:
        print(f"Failed to remove user '{user_id}' from group '{group_id}': HTTP {resp.status_code} {resp.text}")
        return False


def add_user_to_group_by_userid(user_id: str, group_id: str) -> bool:
    if not group_id:
        print("add_user_to_group_by_userid: empty group_id")
        return False
    group_details = load_group_members(group_id)
    members = group_details["members"]
    group_path = group_details["path"]

    if not group_path:
        print(f"None path for group - {group_id}")
        return False
    if members is None:
        MEMBERS[group_id]["members"] = list()
        members = MEMBERS[group_id]["members"]
        
    #print(f"{group_id} - {members}")

    uuid = load_uuid(user_id)

    if uuid in members:
        print(f"User '{user_id}' (uuid: {uuid}) already in group '{group_id}'")
        return True

    url = f"{BASE_URL}{group_path}.rw.html"
    data = {"addMembers": user_id}
    try:
        resp = requests.post(url, data=data, auth=HTTPBasicAuth(*AUTH), timeout=TIMEOUT)
    except Exception as e:
        print(f"Failed to add user '{user_id}' to group '{group_id}': {e}")
        return False

    if resp.status_code in (200, 201):
        members.append(uuid)
        print(f"Added user '{user_id}' (uuid: {uuid}) to group '{group_id}'")
        #print(f"{group_id} - {members}")
        return True
    else:
        print(f"Failed to add user '{user_id}' to group '{group_id}': HTTP {resp.status_code} {resp.text}")
        return False

def read_and_create_users_from_excel(path: str = "test.xlsx"):
    df = pd.read_excel(path, dtype=str, header=0).fillna("")
    if df.shape[1] < 3:
        raise ValueError("Excel must have at least three columns for email_id, first name and last name")

    for idx in range(len(df)):
        row = df.iloc[idx]
        user_id = str(row.iloc[0]).strip()
        first_name = str(row.iloc[1]).strip() if df.shape[1] > 1 else ""
        last_name = str(row.iloc[2]).strip() if df.shape[1] > 2 else ""
        groups_cell = str(row.iloc[3]).strip() if df.shape[1] > 3 else ""

        groups = [g.strip() for g in groups_cell.split(",") if g.strip()] if groups_cell else []
        for group_id in groups:
            load_group_members(group_id)
        print(f"[{idx}] Creating user '{user_id}' (givenName='{first_name}', familyName='{last_name}'), groups parsed: {groups}")

        try:
            resp = create_user(user_id, first_name, last_name)
            print(f"[{idx}] HTTP {resp.status_code}")
        except Exception as e:
            print(f"[{idx}] Exception while creating user '{user_id}': {e}")
            continue

def read_and_add_to_groups_from_excel(path: str = "test.xlsx"):
    df = pd.read_excel(path, dtype=str, header=0).fillna("")
    if df.shape[1] < 3:
        raise ValueError("Excel must have at least three columns for email_id, first name and last name")

    for idx in range(len(df)):
        row = df.iloc[idx]
        user_id = str(row.iloc[0]).strip()
        groups_cell = str(row.iloc[3]).strip() if df.shape[1] > 3 else ""

        groups = [g.strip() for g in groups_cell.split(",") if g.strip()] if groups_cell else []
        for group_id in groups:
            load_group_members(group_id)

        for group_id in groups:
            if not group_id:
                continue
            added = add_user_to_group_by_userid(user_id, group_id)
            print(f"[{idx}] add to '{group_id}': {added}")


def read_and_replicate_access_from_excel(path: str = "test.xlsx"):
    df = pd.read_excel(path, dtype=str, header=0).fillna("")
    if df.shape[1] < 2:
        raise ValueError("Excel must have at least 2 columns for 1. user id and 2. to be replicate from user id")

    for idx in range(len(df)):
        row = df.iloc[idx]
        user_id = str(row.iloc[0]).strip()
        replicate_from_id = str(row.iloc[1]).strip() if df.shape[1] > 1 else ""
        groups = groups_having_id(replicate_from_id)
        if groups is not None:
            for group_id in groups:
                if not group_id:
                    continue
                added = add_user_to_group_by_userid(user_id, group_id)
                print(f"[{idx}] add to '{group_id}': {added}")


def read_and_create_users_and_add_to_groups_from_excel(path: str = "test.xlsx"):
    df = pd.read_excel(path, dtype=str, header=0).fillna("")
    if df.shape[1] < 3:
        raise ValueError("Excel must have at least three columns for email_id, first name and last name")

    for idx in range(len(df)):
        row = df.iloc[idx]
        user_id = str(row.iloc[0]).strip()
        first_name = str(row.iloc[1]).strip() if df.shape[1] > 1 else ""
        last_name = str(row.iloc[2]).strip() if df.shape[1] > 2 else ""
        groups_cell = str(row.iloc[3]).strip() if df.shape[1] > 3 else ""

        groups = [g.strip() for g in groups_cell.split(",") if g.strip()] if groups_cell else []
        for group_id in groups:
            load_group_members(group_id)
        print(f"[{idx}] Creating user '{user_id}' (givenName='{first_name}', familyName='{last_name}'), groups parsed: {groups}")

        try:
            resp = create_user(user_id, first_name, last_name)
            print(f"[{idx}] HTTP {resp.status_code}")
        except Exception as e:
            print(f"[{idx}] Exception while creating user '{user_id}': {e}")
            continue

        for group_id in groups:
            if not group_id:
                continue
            added = add_user_to_group_by_userid(user_id, group_id)
            print(f"[{idx}] add to '{group_id}': {added}")


def read_and_remove_users_from_groups_from_excel(path: str = "test.xlsx"):
    df = pd.read_excel(path, dtype=str, header=0).fillna("")
    if df.shape[1] < 3:
        raise ValueError("Excel must have at least three columns for email_id, first name and last name")

    for idx in range(len(df)):
        row = df.iloc[idx]
        user_id = str(row.iloc[0]).strip()
        groups_cell = str(row.iloc[3]).strip() if df.shape[1] > 3 else ""

        groups = [g.strip() for g in groups_cell.split(",") if g.strip()] if groups_cell else []
        for group_id in groups:
            load_group_members(group_id)

        for group_id in groups:
            if not group_id:
                continue
            removed = remove_user_from_group_by_userid(user_id, group_id)
            print(f"[{idx}] Remove {user_id} from '{group_id}': {removed}")


if __name__ == "__main__":
    #read_and_create_users_and_add_to_groups_from_excel("test.xlsx")
    #read_and_create_users_from_excel("test.xlsx")
    read_and_add_to_groups_from_excel("test.xlsx")
    #read_and_remove_users_from_groups_from_excel("test.xlsx")
    #read_and_replicate_access_from_excel("test_r.xlsx")
    print("Program Ran Successfully")