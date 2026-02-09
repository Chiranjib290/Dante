# import requests

# query="https://dpe-stg.pwc.com/bin/querybuilder.json?1_property=sling%3aresourceType&1_property.operation=like&1_property.value=%25summary-explorer%25&p.hits=selective&p.limit=-1&p.properties=jcr%3apath&path=%2fcontent%2fpwc%2fde"
# response = requests.get(query, auth=("chiranjib.bhattacharyya@in.pwc.com", "Change@123456"), timeout = 120.0)
# out_val = response.json()

# for i in out_val["hits"]:
#     data=i["jcr:path"]
#     print(data)


import requests
from openpyxl import Workbook

# Query to get data
query = "https://dpe-stg.pwc.com/bin/querybuilder.json?1_property=sling%3aresourceType&1_property.operation=like&1_property.value=%25summary-explorer%25&p.hits=selective&p.limit=-1&p.properties=jcr%3apath&path=%2fcontent%2fpwc%2fde"
response = requests.get(query, auth=("chiranjib.bhattacharyya@in.pwc.com", "Change@123456"), timeout=120.0)
out_val = response.json()

# Create a new workbook and select the active worksheet
wb = Workbook()
ws = wb.active
ws.title = "Data Output"

# Write data to the Excel file
ws.append(["Path"])  # Adding a header row
for i in out_val["hits"]:
    data = i["jcr:path"]
    ws.append([data])  # Appending data to the worksheet

# Save the Excel file
output_file = "output_data.xlsx"
wb.save(output_file)
print(f"Data successfully written to {output_file}")
