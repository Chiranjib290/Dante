import requests
import json
import csv

# Set your API credentials and data center
CLIENT_ID = '05b9e14d17cb90dff868fd28df515835'
CLIENT_SECRET = 'gwswig6gMBLZfH81zREWWxenm9ZFEp4jziUUTTSOWBLO5HsP8oUl9Y6H09LCnLok'
DATA_CENTER = 'fra1'

# Generate access token
def get_access_token():
    url = f"https://{DATA_CENTER}.qualtrics.com/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.json()["access_token"]

# Fetch license usage details
def fetch_license_usage(access_token):
    url = f"https://{DATA_CENTER}.qualtrics.com/API/v3/administration/license-usage"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Export data to CSV
def export_to_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the headers
        writer.writerow(['Field1', 'Field2', 'Field3'])  # Adjust field names as needed
        # Write the data
        for item in data['result']:  # Adjust based on the actual structure
            writer.writerow([item['field1'], item['field2'], item['field3']])  # Adjust field names as needed

# Main function
def main():
    access_token = get_access_token()
    license_usage_data = fetch_license_usage(access_token)
    print(json.dumps(license_usage_data, indent=2))  # Diagnostic print statement
    export_to_csv(license_usage_data, 'license_usage_details.csv')

if __name__ == "__main__":
    main()
