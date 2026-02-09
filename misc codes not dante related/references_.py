import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

# 1. Configuration
USERNAME    = "chiranjib.bhattacharyya@in.pwc.com"
PASSWORD    = "Change@123456"
REF1        = "/content/pwc/us/en/industries/energy-utilities-resources.html"
REF2        = "/content/pwc/us/en/industries/industrial-products.html"
AEM_BASE    = "http://10.248.53.101:4502"
QUERY_ENDPOINT = "/crx/de/query.jsp"
OUTPUT_FILE = "Report_References2.xlsx"

DEFAULT_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "python-requests/2.x"
}

def url_is_reachable(url, timeout=5):
    try:
        response = requests.get(url, allow_redirects=False, timeout=timeout)
        if response.status_code != 200:
            return False

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        if title.lower() == "404":
            return False

        return True
    except Exception:
        return False


# -------------------------------
# SQL QUERY EXECUTION
# -------------------------------

def _build_query_params(sql_stmt, dc=None, charset="utf-8", type_="sql", showResults="true"):
    return {
        "_dc": dc if dc is not None else "0",
        "_charset_": charset,
        "type": type_,
        "stmt": sql_stmt,
        "showResults": showResults
    }

def _clean_path(path):
    marker = "/jcr:content/"
    if marker in path:
        return path.split(marker, 1)[0]
    return path

def run_sql_query(path):
    """
    Executes:
    select * from nt:base where contains(*, '<path>')
    Returns list of cleaned paths.
    """
    sql_stmt = f"select * from nt:base where contains(*, '{path}')"
    url = AEM_BASE.rstrip("/") + QUERY_ENDPOINT
    params = _build_query_params(sql_stmt)

    try:
        resp = requests.get(
            url,
            params=params,
            headers=DEFAULT_HEADERS,
            auth=HTTPBasicAuth(USERNAME, PASSWORD),
            timeout=30,
            verify=True
        )
    except requests.RequestException:
        return []

    if resp.status_code != 200:
        return []

    try:
        data = resp.json()
    except ValueError:
        return []

    results = data.get("results") or []
    cleaned = []

    for item in results:
        raw_path = item.get("path")
        if raw_path:
            cleaned.append((raw_path))

    return cleaned


# -------------------------------
# PROCESSING LOGIC
# -------------------------------

def split_items(paths, record, refer):
    pages = []
    fragments = []

    if not record:
        record = {
            "Path (Referenced)": refer,
            "Ref : XF URL": "",
            "Ref : XF Component Path": "",
            "XF Path": ""
        }

    frag_record = {"Path (Referenced)": refer}

    for full_path in paths:
        if "/jcr:content/" in full_path:
            base, component = full_path.split("/jcr:content/", 1)
        else:
            base, component = full_path, ""

        if "experience-fragments" in base:
            frag_record["Ref : XF URL"] = "https://www.pwc.com" + base + ".html"
            frag_record["XF Path"] = base
            frag_record["Ref : XF Component Path"] = component
            fragments.append(frag_record.copy())
        else:
            # Build country-specific URL
            if "/content/pwc/za" in base:
                t = "pwc.co.za" + base.split("/content/pwc/za")[-1]
            elif "/content/pwc/tr" in base:
                t = "pwc.com.tr" + base.split("/content/pwc/tr")[-1]
            elif "/content/pwc/ie/en" in base:
                t = "pwc.ie" + base.split("/content/pwc/ie/en")[-1]
            elif "/content/pwc/es" in base:
                t = "pwc.es" + base.split("/content/pwc/es")[-1]
            elif "/content/pwc/au/en" in base:
                t = "pwc.com.au" + base.split("/content/pwc/au/en")[-1]
            else:
                t = "pwc.com" + base.split("/content/pwc")[-1]

            link = f"https://www.{t}.html"

            if url_is_reachable(link):
                record["Ref : URL"] = link
                record["Ref : Component Path"] = component
                pages.append(record.copy())

    return pages, fragments


def main2(refer):
    # First-level references
    paths = run_sql_query(refer)
    pages, fragments = split_items(paths, False, refer)

    # Second-level XF references
    for f in fragments:
        xf_paths = run_sql_query(f["XF Path"])
        pages1, frags = split_items(xf_paths, f, refer)
        pages.extend(pages1)

    return pages


# -------------------------------
# WRITE EXCEL
# -------------------------------

def write_excel(pages, filename):
    df_pages = pd.DataFrame(pages)

    desired_order = [
        "Path (Referenced)",
        "Ref : URL",
        "Ref : Component Path",
        "Ref : XF URL",
        "Ref : XF Component Path"
    ]

    df_pages = df_pages.drop(columns=["XF Path"], errors="ignore")
    df_pages = df_pages.drop_duplicates()

    for col in desired_order:
        if col not in df_pages.columns:
            df_pages[col] = ""

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


# -------------------------------
# MAIN
# -------------------------------

if __name__ == "__main__":
    l1 = main2(REF1)
    l2 = main2(REF2)
    pages = l1 + l2
    write_excel(pages, OUTPUT_FILE)
