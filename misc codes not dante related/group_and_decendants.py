import requests
from requests.auth import HTTPBasicAuth
from collections import defaultdict

# Configuration
BASE_URL = "https://auth-valuestore-qa.pwc.com/bin/querybuilder.json"
AUTH     = HTTPBasicAuth("chiranjib.bhattacharyya@pwc.com", "Change@123456")


def build_group_hierarchy(base_url=BASE_URL, auth=AUTH):
    """
    Fetches all rep:Group nodes under /home/groups via QueryBuilder,
    then builds and returns a dict mapping each group’s principalName
    to a sorted list of itself plus all of its descendant groups.
    """
    # 1. Pull all rep:Group nodes
    params = {
        "path":        "/home/groups/",
        "type":        "rep:Group",
        "p.hits":      "selective",
        "p.limit":     "-1",
        "p.properties":"rep:principalName jcr:uuid rep:members"
    }
    resp = requests.get(base_url, params=params, auth=auth)
    resp.raise_for_status()
    hits = resp.json().get("hits", [])

    # 2. Build uuid→name & raw group→parent-UUIDs maps
    uuid_to_name    = {}
    parents_by_grp  = {}
    for hit in hits:
        uuid = hit.get("jcr:uuid")
        name = hit.get("rep:principalName")
        if not (uuid and name):
            continue
        uuid_to_name[uuid] = name

        raw = hit.get("rep:members", [])
        if isinstance(raw, str):
            parent_uuids = [raw]
        else:
            parent_uuids = list(raw)
        parents_by_grp[name] = parent_uuids

    # 3. Invert to build parent_name → [child_name, …]
    children_map = defaultdict(list)
    for grp_name, parent_uuids in parents_by_grp.items():
        # ensure every group appears in children_map, even if it has no children
        children_map.setdefault(grp_name, [])
        for pu in parent_uuids:
            parent_name = uuid_to_name.get(pu)
            if parent_name:
                children_map[parent_name].append(grp_name)

    # 4. Recursively collect descendants
    def collect_descendants(group, seen=None):
        if seen is None:
            seen = set()
        if group in seen:
            return set()
        seen.add(group)

        result = {group}
        for child in children_map.get(group, []):
            result |= collect_descendants(child, seen)
        return result

    # 5. Build and return the final hierarchy dict
    return {
        grp: sorted(collect_descendants(grp))
        for grp in children_map
    }


# Optional: globally available hierarchy at import time
GROUP_HIERARCHY = build_group_hierarchy()

if __name__ == "__main__":
    import json
    # Print the hierarchy for inspection
    #print(json.dumps(GROUP_HIERARCHY, indent=2))
    print(GROUP_HIERARCHY["vs-gx-authors"])
