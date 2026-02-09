import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

AEM_BASE = "http://10.248.53.101:4502"
QUERY_ENDPOINT = "/crx/de/query.jsp"

USERNAME = "chiranjib.bhattacharyya@in.pwc.com"
PASSWORD = "Change@123456"

INPUT_FILE  = "test.xlsx"
OUTPUT_FILE = "output3.xlsx"

DEFAULT_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "python-requests/2.x"
}


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


def run_sql_query(payload_path):
    """
    Executes:
    select * from nt:base where contains(*, '<payload>')
    """
    sql_stmt = f"select * from nt:base where contains(*, '{payload_path}')"

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
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

    if resp.status_code != 200:
        print(f"AEM returned {resp.status_code}: {resp.text[:300]}")
        return []

    try:
        data = resp.json()
    except ValueError:
        print("Invalid JSON returned")
        return []

    results = data.get("results") or []
    cleaned = []
    for item in results:
        raw_path = item.get("path")
        if raw_path:
            cleaned.append(_clean_path(raw_path))

    return cleaned


def process_excel():
    df = pd.read_excel(INPUT_FILE)

    df["References"] = df["Payload"].apply(run_sql_query)

    df.to_excel(OUTPUT_FILE, index=False)
    print(f"Completed. Output saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    process_excel()
