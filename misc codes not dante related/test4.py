import requests
from urllib.parse import urljoin
import io, zipfile

AEM_BASE = "https://auth-valuestore-qa.pwc.com/"
USER = "chiranjib.bhattacharyya@pwc.com"
PWD = "Change@123456"
TARGET = "bulk-import-20251022-1.0"

s = requests.Session()
s.auth = (USER, PWD)
s.headers.update({"User-Agent": "python-requests/2.x"})

# 1. list all packages
r = s.get(urljoin(AEM_BASE, "/crx/packmgr/service.jsp"), params={"cmd":"ls"}, timeout=30)
print("ls status", r.status_code)
body = r.text
print(body[:2000])

# 2. attempt to find any occurrence of TARGET in listing
if TARGET in body:
    print("Found target text in listing output")
else:
    print("Target not found in listing output")

# 3. try to download the package if PackMgr knows it at some other group
# We'll try to search for packageName values in the listing output and try get on them
import re
names = re.findall(r"<name>([^<]+)</name>\s*<version>([^<]+)</version>\s*<group>([^<]+)</group>", body)
attempts = []
for name, version, group in names:
    full = f"{group}/{name}-{version}"
    if TARGET.split("-",1)[0] in name or TARGET in full:
        attempts.append(full)

# Try download on any candidate full ids and also try the exact target
candidates = list(dict.fromkeys(attempts + [f"my_packages/{TARGET}"]))
for pkg in candidates:
    print("Trying download for", pkg)
    r2 = s.get(urljoin(AEM_BASE, "/crx/packmgr/service.jsp"), params={"cmd":"get","packageName":pkg}, timeout=30, stream=True)
    print("->", r2.status_code, r2.headers.get("content-type"))
    if r2.status_code == 200 and 'application/zip' in (r2.headers.get('content-type') or ''):
        data = r2.content
        print("Downloaded zip size", len(data))
        z = zipfile.ZipFile(io.BytesIO(data))
        print("Zip list:", z.namelist())
        break
else:
    print("No downloadable package found among candidates.")
