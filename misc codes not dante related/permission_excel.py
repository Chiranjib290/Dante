from collections import defaultdict
import requests
from requests.auth import HTTPBasicAuth
from fnmatch import fnmatch
import os

# 1. Base QueryBuilder URL but *without* the principalName filter
BASE_URL = "https://auth-valuestore-qa.pwc.com/bin/querybuilder.json"
COMMON_PARAMS = {
    "group.1_property":        "jcr:primaryType",
    "group.1_property.value":  "rep:GrantACE",
    "group.2_property":        "jcr:primaryType",
    "group.2_property.value":  "rep:DenyACE",
    "group.p.or":              "true",
    "p.hits":                  "selective",
    "p.limit":                 "-1",
    "p.properties":            "jcr:path jcr:primaryType "
                                "rep:principalName rep:privileges "
                                "rep:restrictions/rep:glob"
}

AUTH = HTTPBasicAuth(
    "chiranjib.bhattacharyya@pwc.com",
    "Change@123456"
)

# 2. Capability names in the requested order
CAPABILITY_MAP = {
    "Read":      ["jcr:read"],
    "Modify":    ["jcr:modifyProperties"],
    "Create":    ["jcr:addChildNodes"],
    "Delete":    ["jcr:removeNode", "jcr:removeChildNodes"],
    "Read ACL":  ["jcr:readAccessControl"],
    "Edit ACL":  ["jcr:modifyAccessControl"],
    "Replicate": ["crx:replicate", "cq:replicateDelete"]
}

def fetch_aces(principals, search_path):
    """
    Run QueryBuilder once per principal in 'principals' under 'search_path'
    and union all ACE hits.
    """
    all_hits = []
    for principal in principals:
        params = COMMON_PARAMS.copy()
        params["path"] = search_path

        params.update({
            "property":       "rep:principalName",
            "property.value": principal
        })
        resp = requests.get(BASE_URL, params=params, auth=AUTH)
        resp.raise_for_status()
        hits = resp.json().get("hits", [])
        all_hits.extend(hits)

    return all_hits

def ace_applies(ace, target_path):
    # strip /rep:policy/<aceName> to get the protected base path
    ace_path = ace["jcr:path"]
    base = os.path.dirname(os.path.dirname(ace_path))
    if not (target_path == base or target_path.startswith(base.rstrip("/") + "/")):
        return False

    # honor any rep:glob restriction
    glob_pattern = ace.get("rep:restrictions", {}).get("rep:glob")
    if glob_pattern:
        rel = target_path[len(base.rstrip("/")) + 1:]
        return fnmatch(rel, glob_pattern)

    return True

def evaluate_permissions(aces, target_path):
    """
    Merge grants & denies, default-allowing jcr:read unless explicitly denied.
    """
    granted = set()
    denied  = set()

    for ace in aces:
        if not ace_applies(ace, target_path):
            continue

        privs = set(ace.get("rep:privileges", []))
        ptype = ace.get("jcr:primaryType", "")
        if ptype == "rep:DenyACE":
            denied |= privs
        else:
            granted |= privs

    # Default-allow read if no explicit denyACE on jcr:read
    if "jcr:read" not in denied:
        granted.add("jcr:read")

    # denies override grants
    return granted - denied

def print_insights(target_path, group):
    # include the group itself *and* the built-in everyone
    principals = GROUP_HIERARCHY[group]
    #print(f"FAMILY - {principals}")

    # pass target_path as the QueryBuilder "path"
    aces      = fetch_aces(principals, target_path)
    effective = evaluate_permissions(aces, target_path)

    print(f"\nEffective capabilities on {target_path}:\n")
    for name, needed in CAPABILITY_MAP.items():
        ok   = any(p in effective for p in needed)
        mark = "✓" if ok else "✗"
        print(f"  {mark}  {name}")

def build_group_hierarchy(base_url=BASE_URL, auth=AUTH):
    """
    Fetches all rep:Group nodes under /home/groups via QueryBuilder,
    then builds and returns a dict mapping each group’s principalName
    to a sorted list of itself plus all of its descendant groups.
    """
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

    uuid_to_name   = {}
    parents_by_grp = {}
    for hit in hits:
        uuid = hit.get("jcr:uuid")
        name = hit.get("rep:principalName")
        if not (uuid and name):
            continue
        uuid_to_name[uuid]            = name
        raw = hit.get("rep:members", [])
        parents_by_grp[name] = raw if isinstance(raw, list) else [raw]

    children_map = defaultdict(list)
    for grp, parent_uuids in parents_by_grp.items():
        children_map.setdefault(grp, [])
        for pu in parent_uuids:
            parent_name = uuid_to_name.get(pu)
            if parent_name:
                children_map[parent_name].append(grp)

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

    return {
        grp: sorted(collect_descendants(grp))
        for grp in children_map
    }

GROUP_HIERARCHY = build_group_hierarchy()

if __name__ == "__main__":
    node_to_check = "/conf"
    group         = "vs-base-user"
    print_insights(node_to_check, group)
