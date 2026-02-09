import requests

BASE_URL    = 'http://10.196.83.228:4502'
USERNAME    = 'admin'
PASSWORD    = 'B9HbfFTdV2oq15yotZwyowV4dQUJGC'

USER_PATH   = '/home/users/7/7ki9vA7C6ad2Q0knkhr_'
GROUP_PATH  = '/home/groups/O/Oww7GiEv3BDOkjbwCjNu'

REMOVED_IDS = [
    '5d9c68c6-c50e-33d0-aa2f-cf54f63993b6'
]

AUTH    = (USERNAME, PASSWORD)


def delete_user(path):
    url  = f"{BASE_URL}{path}"
    data = {'deleteAuthorizable': ''}
    resp = requests.post(url, data=data, auth=AUTH, timeout=10)
    if resp.status_code == 200:
        print(f"✅ Deleted: {path}")
    else:
        print(f"❌ Failed to delete {path}: {resp.status_code}")
        print(resp.text)


def update_group_members():

    json_url = f"{BASE_URL}{GROUP_PATH}.infinity.json"
    resp     = requests.get(json_url, auth=AUTH, timeout=10)
    resp.raise_for_status()
    data        = resp.json()
    old_members = data.get('rep:members', [])
    print("Current members:", old_members)

    new_members = [
        member for member in old_members
        if not any(uid in member for uid in REMOVED_IDS)
    ]
    print("Filtered members:", new_members)

    payload = [
        ('rep:members@Delete', ''),
        ('rep:members@TypeHint', 'WeakReference[]')
    ]

    for m in new_members: payload.append(('rep:members', m))
    
    print(payload)
    resp = requests.post(
        f"{BASE_URL}{GROUP_PATH}",
        data=payload,                  
        auth=AUTH,
        timeout=10
    )
    resp.raise_for_status()
    print("✅ POST multipart succeeded")
    

if __name__ == "__main__":
    #delete_user(USER_PATH)

    update_group_members()
