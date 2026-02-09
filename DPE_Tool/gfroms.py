import requests
from bs4 import BeautifulSoup
import pandas as pd

excel_file_path = "pages.xlsx" 

df = pd.read_excel(excel_file_path)

url_column = df.columns[0]

search_word = "forms.gle"

anchor_texts = []
href_links = []

for index, row in df.iterrows():
    page_url = row[url_column]
    print(f"Processing: {page_url}")
    try:
        response = requests.get(page_url)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            a_tags = soup.find_all("a")
            
            page_anchor_texts = []
            page_href_links = []

            for tag in a_tags:
                anchor_text = tag.get_text().strip()
                href = tag.get("href", "")

                #these 2 lines ideally would be removed later
                search_word="https"
                if "https://www.pwc.se" not in tag.get("href", "").lower() and (search_word.lower() in href.lower() or search_word.lower() in anchor_text.lower()):
                
                
                #if search_word.lower() in href.lower() or search_word.lower() in anchor_text.lower():
                    page_anchor_texts.append(anchor_text)
                    page_href_links.append(href)

            anchor_texts.append("; ".join(page_anchor_texts) if page_anchor_texts else "")
            href_links.append("; ".join(page_href_links) if page_href_links else "")
        else:
            print(f"Failed to load {page_url} (status code: {response.status_code}).")
            anchor_texts.append("")
            href_links.append("")
    except Exception as e:
        print(f"Error processing {page_url}: {e}")
        anchor_texts.append("")
        href_links.append("")

df["Anchor Text"] = anchor_texts
df["Href Link"] = href_links

output_excel_file = "pages_with_links.xlsx"
df.to_excel(excel_file_path, index=False)

print(f"Results have been written to {excel_file_path}")
