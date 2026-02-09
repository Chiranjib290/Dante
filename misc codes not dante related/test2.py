#!/usr/bin/env python3
# Requirements: requests, pandas, openpyxl
# pip install requests pandas openpyxl

import requests
import pandas as pd
from datetime import datetime
from urllib.parse import urljoin
import time

# ---------- USER CONFIG (from you) ----------
AEM_BASE = "https://auth-valuestore-qa.pwc.com/" 
USERNAME = "chiranjib.bhattacharyya@pwc.com"
PASSWORD = "Change@123456"
PACKAGE_GROUP = "my_packages"
PACKAGE_BASE_NAME = "bulk-import"
EXCEL_FILE = "paths.xlsx"
EXCEL_SHEET = 0
EXCEL_COLUMN = "path"
PACKAGE_VERSION = "1.0"
# retry settings
RETRY_ATTEMPTS = 3
RETRY_BACKOFF = 2.0
# --------------------------------------------

session = requests.Session()
session.auth = (USERNAME, PASSWORD)
session.headers.update({
    "User-Agent": "python-requests/2.x",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
})

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

def fetch_csrf_token():
    token = None
    try:
        url = urljoin(AEM_BASE, "/crx/packmgr/service.jsp")
        headers = {"CSRF-Token": "Fetch"}
        resp = session.post(url, headers=headers, timeout=15, allow_redirects=True)
        token = resp.headers.get("CSRF-Token") or resp.headers.get("csrf-token") or resp.headers.get("X-CSRF-Token")
    except Exception:
        token = None
    if token:
        session.headers.update({"CSRF-Token": token})
    return token

def create_package_via_servicejsp(group, name, version="1.0"):
    url = urljoin(AEM_BASE, "/crx/packmgr/service.jsp")
    data = {
        "cmd": "create",
        "group": group,
        "name": name,
        "version": version,
        "force": "true"
    }
    resp = session.post(url, data=data, timeout=30)
    resp.raise_for_status()
    package_id = f"{group}/{name}-{version}"
    return package_id

def add_filter_to_package(package_id, path):
    url = urljoin(AEM_BASE, "/crx/packmgr/service.jsp")
    data = {
        "cmd": "save",
        "packageName": package_id,
        "filter": path
    }
    if "CSRF-Token" not in session.headers:
        fetch_csrf_token()
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            resp = session.post(url, data=data, timeout=30)
            if 200 <= resp.status_code < 300:
                return True
            if resp.status_code in (429, 503) and attempt < RETRY_ATTEMPTS:
                time.sleep(RETRY_BACKOFF * attempt)
                continue
            return False
        except requests.RequestException:
            if attempt < RETRY_ATTEMPTS:
                time.sleep(RETRY_BACKOFF * attempt)
                continue
            return False
    return False

def main():
    today = datetime.utcnow().strftime("%Y%m%d")
    pkg_name = f"{PACKAGE_BASE_NAME}-{today}"
    try:
        paths = read_paths_from_excel(EXCEL_FILE, sheet=EXCEL_SHEET, column=EXCEL_COLUMN)
    except Exception as e:
        print(f"Failed reading Excel: {e}")
        return

    if not paths:
        print("No paths found in the Excel file.")
        return

    try:
        fetch_csrf_token()
        pkg_id = create_package_via_servicejsp(PACKAGE_GROUP, pkg_name, version=PACKAGE_VERSION)
    except requests.HTTPError as e:
        print(f"Failed to create package: {e} - {getattr(e.response, 'text', '')}")
        return
    except Exception as e:
        print(f"Failed to create package: {e}")
        return

    success_count = 0
    for p in paths:
        ok = add_filter_to_package(pkg_id, p)
        if ok:
            success_count += 1

    print(f"Package created: {PACKAGE_GROUP}/{pkg_name}-{PACKAGE_VERSION}")
    print(f"Paths successfully added to package: {success_count} out of {len(paths)}")

if __name__ == "__main__":
    main()
