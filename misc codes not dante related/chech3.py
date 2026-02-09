import pandas as pd
import requests
from tqdm import tqdm

# 1) Load the workbook
df = pd.read_excel('to_update.xlsx', engine='openpyxl')

# 2) Confirm “Value” is present
assert 'Value' in df.columns, f"'Value' not in columns: {df.columns.tolist()}"

# 3) URL‐check helper
def url_exists(path: str) -> bool:
    if not isinstance(path, str) or not path.strip():
        return False
    url = f"https://dpe.pwc.com/libs/wcm/core/content/pageinfo.json?path={path.strip()}"
    try:
        resp = requests.get(url, auth=("chiranjib.bhattacharyya@in.pwc.com","Change@123456"))
        return resp.status_code == 200
    except requests.RequestException:
        return False

# 4) Apply check across your “Value” column
tqdm.pandas(desc="Checking URLs")
df['keep'] = df['Value'].progress_apply(url_exists)

# 5) Filter & write out the survivors
filtered = df[df['keep']].drop(columns=['keep'])
filtered.to_excel('to_update_filtered.xlsx', index=False, engine='openpyxl')

print(f"✅ Filtered complete: kept {len(filtered)} of {len(df)} rows.")
