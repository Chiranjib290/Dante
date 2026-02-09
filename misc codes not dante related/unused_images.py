import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

USERNAME = "chiranjib.bhattacharyya@in.pwc.com"
PASSWORD = "Change@123456"

INPUT_FILE = "data.xlsx"
OUTPUT_FILE = "result.xlsx"

df_live = pd.read_excel(INPUT_FILE, sheet_name="Live Pages")
df_images = pd.read_excel(INPUT_FILE, sheet_name="Images")

live_pages_set = set(df_live["Payload"].astype(str).str.strip())

unused_images = []
used_images = []  # store tuples: (image, page)

for img_path in df_images["Payload"]:
    img_path = str(img_path).strip()
    print(img_path)
    url = f"https://dpe.pwc.com/bin/wcm/references.json?path={img_path}"

    try:
        resp = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), timeout=20)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"Error fetching {img_path}: {e}")
        unused_images.append(img_path)
        continue

    pages = data.get("pages", [])

    if not pages:
        unused_images.append(img_path)
        continue

    referenced_paths = {p.get("path", "").strip() for p in pages}

    intersection = referenced_paths.intersection(live_pages_set)

    if intersection:
        for p in intersection:
            used_images.append((img_path, p))
    else:
        unused_images.append(img_path)

df_unused = pd.DataFrame({"Unused Images": unused_images})
df_used = pd.DataFrame(used_images, columns=["Image", "Used In Page"])

with pd.ExcelWriter(OUTPUT_FILE) as writer:
    df_unused.to_excel(writer, sheet_name="Unused Images", index=False)
    df_used.to_excel(writer, sheet_name="Used Images", index=False)

print("Done. Saved to result.xlsx")
