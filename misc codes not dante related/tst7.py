
import requests
import pandas as pd

userid = "chiranjib.bhattacharyya@in.pwc.com"
userPassword = "Change@123456"
ip = "https://dpe-qa.pwc.com"
file_path = "Users.xlsx"

def findGroupsOfUsers(file_path):

    df = pd.read_excel(file_path, sheet_name=0)

    groups_list = []

    for email_id in df.iloc[:, 0]:
        if pd.isna(email_id):
            groups_list.append('')
            continue
        email_id = str(email_id)

        try:
            parts = email_id.split("@")
            formatted_email = parts[0] + "%40" + parts[1]
        except Exception as e:
            formatted_email = email_id  # fallback in case the formatting fails

        query1 = (
            f"{ip}/bin/querybuilder.json?"
            "1_property=jcr%3aprimaryType&1_property.value=rep%3aUser&"
            f"2_property=rep%3aprincipalName&2_property.value={formatted_email}&"
            "p.hits=selective&p.properties=jcr%3auuid&path=%2fhome%2fusers"
        )
        response1 = requests.get(query1, auth=(userid, userPassword), timeout=120.0)
        data1 = response1.json()
        
        if not data1.get("hits"):
            groups_list.append('Incorrect Email')
            continue
        
        uuid = data1["hits"][0]["jcr:uuid"]

        query2 = (
            f"{ip}/bin/querybuilder.json?"
            f"property=rep%3amembers&property.value={uuid}&"
            "p.hits=selective&p.properties=jcr%3apath&path=%2fhome%2fgroups"
        )
        response2 = requests.get(query2, auth=(userid, userPassword), timeout=120.0)
        data2 = response2.json()

        groups = ["everyone"]
        for hit in data2.get("hits", []):
            jcr_path = hit.get("jcr:path", "")
            path_parts = jcr_path.split("/")
            if len(path_parts) > 4:
                groups.append(path_parts[4])
                
        group_str = ", ".join(groups)
        groups_list.append(group_str)

    df['Groups'] = groups_list

    df.to_excel("Users.xlsx", index=False)

    print("Excel file Updated !")

findGroupsOfUsers(file_path)