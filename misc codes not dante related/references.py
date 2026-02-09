import requests
import pandas as pd
from bs4 import BeautifulSoup

# 1. Configuration
USERNAME    = "chiranjib.bhattacharyya@in.pwc.com"
PASSWORD    = "Change@123456"
REF1        = "/content/pwc/us/en/industries/energy-utilities-resources.html"
REF2        = "/content/pwc/us/en/industries/industrial-products.html"
URL         = f"http://10.248.53.101:4502/bin/wcm/references.json?path="
OUTPUT_FILE = "Report_References.xlsx"

def url_is_reachable(url, timeout=5):
    try:
        response = requests.get(url, allow_redirects=False, timeout=timeout)

        # If it's not HTTP 200, it's not reachable
        if response.status_code != 200:
            return False

        # Parse the HTML title
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else ""

        # If the title indicates a 404 page, treat as unreachable
        if title.lower() == "404":
            return False

        return True

    except Exception:
        return False
    
def fetch_json(url,ref, username, password):
    resp = requests.get(url+ref, auth=(username, password))
    resp.raise_for_status()
    return resp.json()

def split_items(data,record,refer):
    pages = []
    fragments = []
    if not record:
        record = {
                    "Path (Referenced)" : refer,
                    "Ref : XF URL" : "",
                    "Ref : XF Component Path" : "",
                    "XF Path":""
                    }
    frag_record = {
                "Path (Referenced)" : refer,
            }
    for items in data.values():
        for item in items:
            path      = item.get("path", "")
            refs      = item.get("references", [])
            src       = item.get("srcPath","")

            if src!=path:              
                #if "experience-fragments" in path: record["references"] = refs
                for r in refs:
                    multiples = r.split("/jcr:content/")
                    if "experience-fragments" in path:
                        frag_record["Ref : XF URL"] = "https://www.pwc.com" + multiples[0] + ".html"
                        frag_record["XF Path"] = multiples[0]
                        frag_record["Ref : XF Component Path"] = multiples[1]
                        fragments.append(frag_record.copy())
                    else:
                        if "/content/pwc/za" in multiples[0]:
                            t = "pwc.co.za"+multiples[0].split("/content/pwc/za")[-1]
                        elif "/content/pwc/tr" in multiples[0]:
                            t = "pwc.com.tr"+multiples[0].split("/content/pwc/tr")[-1]
                        elif "/content/pwc/ie/en" in multiples[0]:
                            t = "pwc.ie"+multiples[0].split("/content/pwc/ie/en")[-1]
                        elif "/content/pwc/es" in multiples[0]:
                            t = "pwc.es"+multiples[0].split("/content/pwc/es")[-1]
                        elif "/content/pwc/au/en" in multiples[0]:
                            t = "pwc.com.au"+multiples[0].split("/content/pwc/au/en")[-1]
                        else:
                            t= "pwc.com"+multiples[0].split("/content/pwc")[-1]
                        link = f"https://www.{t}.html"
                        
                        if url_is_reachable(link):
                            record["Ref : URL"] = link
                            record["Ref : Component Path"] = multiples[1]
                            pages.append(record.copy())
                
    return pages, fragments

def write_excel(pages, filename):
    df_pages = pd.DataFrame(pages)

    # Columns you want to keep and in this exact order
    desired_order = [
        "Path (Referenced)",
        "Ref : URL",
        "Ref : Component Path",
        "Ref : XF URL",
        "Ref : XF Component Path"
    ]

    # Drop unwanted column
    df_pages = df_pages.drop(columns=["XF Path"], errors="ignore")

    # Remove duplicates
    df_pages = df_pages.drop_duplicates()

    # Ensure all expected columns exist (create empty ones if missing)
    for col in desired_order:
        if col not in df_pages.columns:
            df_pages[col] = ""

    # Reorder columns
    df_pages = df_pages[desired_order]

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        df_pages.to_excel(
            writer,
            sheet_name="data",
            index=False,
            header=False,
            startrow=1
        )
        ws1 = writer.sheets["data"]
        for idx, col in enumerate(df_pages.columns, start=1):
            ws1.cell(row=1, column=idx, value=col)


def main2(refer):
    data = fetch_json(URL, refer, USERNAME, PASSWORD)
    pages, fragments = split_items(data,False,refer)
    for f in fragments:
        data = fetch_json(URL, f['XF Path'], USERNAME, PASSWORD)
        pages1, frags = split_items(data,f,refer)
        for p in pages1:
            pages.append(p)
        for fff in frags: print(fff)
    print(pages)
    return pages

if __name__ == "__main__":
    l1 = main2(REF1)
    l2 = main2(REF2)
    pages = l1 + l2
    write_excel(pages, OUTPUT_FILE)
