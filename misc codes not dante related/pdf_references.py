import requests
import pandas as pd

USERNAME    = "chiranjib.bhattacharyya@in.pwc.com"
PASSWORD    = "Change@123456"
URL         = "http://10.248.53.101:4502/bin/wcm/references.json?path="
INPUT_FILE  = "test.xlsx"
OUTPUT_FILE = "output2.xlsx"


def fetch_json(url, ref, username, password):
    resp = requests.get(url + ref, auth=(username, password))
    resp.raise_for_status()
    return resp.json()


def references(data):
    pages = []
    for items in data.values():
        for item in items:
            path = item.get("path", "")
            refs = item.get("references", [])
            src  = item.get("srcPath", "")
            if src != path:
                for r in refs:
                    pload = r.split("/jcr:content/")[0]
                    pages.append(pload)
    return pages


def main2(refer):
    data = fetch_json(URL, refer, USERNAME, PASSWORD)
    pages = references(data)
    return pages


def process_excel():
    # Read Excel file
    df = pd.read_excel(INPUT_FILE)

    # Apply main2 to Payload column
    df["References"] = df["Payload"].apply(main2)

    # Write output
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"Processing complete. Output saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    process_excel()
