import json, requests

BASE      = 'https://auth-brandsite-qa.pwc.com'
AUTH      = ('admin', 'B9HbfFTdV2oq15yotZwyowV4dQUJGC')
GROUPPATH = '/home/groups/O/Oww7GiEv3BDOkjbwCjNu'

def update_group_members():
    # 1) fetch
    r = requests.get(f"{BASE}{GROUPPATH}.infinity.json", auth=AUTH)
    r.raise_for_status()
    members = r.json().get('rep:members', [])
    # 2) filter
    to_remove = ['5d9c68c6-c50e-33d0-aa2f-cf54f63993b6']
    new = [m for m in members if not any(uid in m for uid in to_remove)]
    # 3) merge
    payload = {"rep:members": new}
    r2 = requests.post(
        f"{BASE}{GROUPPATH}.json",
        auth=AUTH,
        headers={'Content-Type':'application/json'},
        data=json.dumps(payload)
    )
    r2.raise_for_status()
    print("✅ members updated via JSON merge")

update_group_members()