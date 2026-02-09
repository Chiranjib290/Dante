#import pandas as pd
import requests

""" def check_url_exists(url):
    try:
        response = requests.head(url, allow_redirects=True)
        #print(url)
        if 200 <= response.status_code < 300:
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False

def check_urls_from_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name=0)
    
    # Iterate through the URLs in the first column (starting from the second row)
    for url in df.iloc[1:, 0]:
        if not check_url_exists(url):
            print(f"CANNOT REACH this = {url}") """

# Example usage
#file_path = "DPE Contact Bio pages (1).xlsx"
#check_urls_from_excel(file_path)


try:
    aborted = requests.post(f"https://dpe-qa.pwc.com/var/workflow/instances/server2/2025-04-08/ChangeTemplate_556", data={'state': 'ABORTED'}, auth=("chiranjib.bhattacharyya@in.pwc.com", "Change@123456"))
    if not (aborted.status_code >= 200 and aborted.status_code <= 205):
        print(f"Failed to Terminate Workflow for URI {aborted.status_code}") 
    else:
        print(f"Success : {aborted.status_code}")       
except Exception as e:
    print(f"Request exception for URI {e}")