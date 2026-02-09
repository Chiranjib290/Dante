""" import requests
from bs4 import BeautifulSoup
 
 
 
page_path = "https://www.pwc.com/se/sv/cfo/cfo-entreprenor.html"  # Path to the page
 # AEM credentials (only needed for author or protected publish)
 
 
response = requests.get(page_path)
 
if response.status_code == 200:
    html_content = response.text
 
#print(html_content)
soup = BeautifulSoup(html_content, "html.parser")
 
a_tags = soup.find_all("a")
 
#print(a_tags)
 
search_word = "forms.gle"  
found = False
 
for tag in a_tags:
    if search_word.lower() in tag.get_text().lower():
            found = True
            print(tag)
            print(f"'{search_word}' found in link text: {tag.get_text()}")
       
    elif search_word.lower() in tag.get("href", "").lower():
            found = True
            print(tag)
            print(f"'{search_word}' found in link URL: {tag.get('href')}") """
 
    #if not found:print(f"'{search_word}' was NOT found in any <a> tags.")
    #else: print(f"Failed to fetch the page. Status code: {response.status_code}") 



import requests
from bs4 import BeautifulSoup

page_path = "https://www.pwc.com/se/sv/cfo/cfo-entreprenor.html"
response = requests.get(page_path)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    a_tags = soup.find_all("a")

    search_word = "forms.gle"
    found = False

    for tag in a_tags:
        # Extract the anchor text and href attribute
        anchor_text = tag.get_text().strip()
        href = tag.get("href", "")

        # Check if the search word is in either the URL or the anchor text
        if search_word.lower() in href.lower() or search_word.lower() in anchor_text.lower():
            found = True
            print("Found link:")
            print("Anchor text:", anchor_text)
            print("URL:        ", href)
            print()  # For readability (blank line)

    if not found:
        print(f"No links found containing '{search_word}'.")
else:
    print("Page did not load correctly. Status code:", response.status_code)
