#!/usr/bin/env python3
# Requirements: requests, pandas, openpyxl
# pip install requests pandas openpyxl

import io
import zipfile
import requests
import pandas as pd
from datetime import datetime
from urllib.parse import urljoin

# ---------- USER CONFIG ----------
AEM_BASE = "https://auth-valuestore-qa.pwc.com/"
USERNAME = "chiranjib.bhattacharyya@pwc.com"
PASSWORD = "Change@123456"
PACKAGE_GROUP = "my_packages"
PACKAGE_BASE_NAME = "bulk-import"
EXCEL_FILE = "paths.xlsx"
EXCEL_SHEET = 0
EXCEL_COLUMN = "path"
PACKAGE_VERSION = "1.0"
# ---------------------------------

session = requests.Session()
session.auth = (USERNAME, PASSWORD)
session.headers.update({"User-Agent": "python-requests/2.x"})

def read_paths_from_excel(excel_file, sheet=0, column="path"):
    df = pd.read_excel(excel_file, sheet_name=sheet, engine="openpyxl")
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found. Available columns: {list(df.columns)}")
    raw = df[column].dropna().astype(str).str.strip()
    seen = set()
    paths = []
    for p in raw:
        if not p:
            continue
        if p in seen:
            continue
        seen.add(p)
        paths.append(p)
    return paths

def build_package_zip_bytes(group, name, version, paths):
    """
    Build an in-memory zip for an AEM package with:
    - META-INF/vault/filter.xml
    - META-INF/vault/properties.xml
    Returns bytes of the zip.
    """
    # construct filter.xml according to Vault filter format
    # simple format: <workspaceFilter version="1.0"><filter root="/path"/></workspaceFilter>
    filter_entries = "\n".join([f'    <filter root="{p}"/>' for p in paths])
    filter_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<workspaceFilter version="1.0">\n{filter_entries}\n</workspaceFilter>\n'

    # properties.xml minimal required fields for Package Manager
    # name should not include version suffix; we'll pass version separately
    properties_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">\n'
        '<properties>\n'
        f'  <entry key="group">{group}</entry>\n'
        f'  <entry key="name">{name}</entry>\n'
        f'  <entry key="version">{version}</entry>\n'
        '  <entry key="packageFormat">2</entry>\n'
        '</properties>\n'
    )

    mem = io.BytesIO()
    with zipfile.ZipFile(mem, mode="w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("META-INF/vault/filter.xml", filter_xml)
        z.writestr("META-INF/vault/properties.xml", properties_xml)
    mem.seek(0)
    return mem.read()

def upload_package_zip(zip_bytes, upload_name, install=False):
    """
    Upload the package zip to PackMgr via service.jsp cmd=upload.
    Returns server response object.
    """
    url = urljoin(AEM_BASE, "/crx/packmgr/service.jsp")
    params = {"cmd": "upload"}
    files = {
        "file": (f"{upload_name}.zip", zip_bytes, "application/zip")
    }
    data = {}
    if install:
        data["install"] = "true"
    resp = session.post(url, params=params, files=files, data=data, timeout=60)
    resp.raise_for_status()
    return resp

def list_packages_for_group(group):
    url = urljoin(AEM_BASE, "/crx/packmgr/service.jsp")
    params = {"cmd": "ls", "group": group}
    resp = session.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.text

def main():
    today = datetime.utcnow().strftime("%Y%m%d")
    pkg_name = f"{PACKAGE_BASE_NAME}-{today}"
    try:
        paths = read_paths_from_excel(EXCEL_FILE, sheet=EXCEL_SHEET, column=EXCEL_COLUMN)
    except Exception as e:
        print("Failed reading Excel:", e)
        return

    if not paths:
        print("No paths found in the Excel file.")
        return

    zip_bytes = build_package_zip_bytes(PACKAGE_GROUP, pkg_name, PACKAGE_VERSION, paths)
    upload_name = f"{pkg_name}-{PACKAGE_VERSION}"  # uploaded filename (AEM uses file metadata to derive package id)

    try:
        resp = upload_package_zip(zip_bytes, upload_name, install=False)
    except requests.HTTPError as e:
        print("Upload failed:", e, "-", getattr(e.response, "text", "")[:1000])
        return
    except Exception as e:
        print("Upload failed:", e)
        return

    # After upload, list group to verify presence
    try:
        listing = list_packages_for_group(PACKAGE_GROUP)
    except Exception as e:
        print("Failed to list packages:", e)
        return

    # Basic check: look for the package name/version text in the listing response
    expected_id = f"{PACKAGE_GROUP}/{pkg_name}-{PACKAGE_VERSION}"
    found = expected_id in listing or f"{pkg_name}-{PACKAGE_VERSION}" in listing

    print("Upload response status:", resp.status_code)
    print("Expected package id:", expected_id)
    print("Package present in PackMgr listing for group:", "YES" if found else "NO")
    print(f"Paths packaged: {len(paths)}")
    if not found:
        print("PackMgr listing (first 2000 chars):")
        print(listing[:2000])

if __name__ == "__main__":
    main()
