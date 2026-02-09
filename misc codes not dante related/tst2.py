from azure.storage.blob import BlobClient
import os

# Define the file name and the local path
file_name = 'obscene.xlsx'
file_path = os.path.join(os.getcwd(), file_name)  # Path to your Excel file in the current directory

# Base URL for the container
container_url = "https://teststoragedante.blob.core.windows.net/testcontainer"

# SAS token for the container
sas_token = "sp=racwdl&st=2025-02-01T07:56:25Z&se=2026-02-01T15:56:25Z&spr=https&sv=2022-11-02&sr=c&sig=P41gFPdWfoUh87VVEkISK0mt8gGQehoOe2jX1gFfIHc%3D"

# Construct the full blob URL
blob_url = f"{container_url}/{file_name}?{sas_token}"

# Create a BlobClient
blob_client = BlobClient.from_blob_url(blob_url)

# Upload the file
with open(file_path, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print("File uploaded successfully!")
