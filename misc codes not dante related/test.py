import os
import csv
import re
import pandas as pd

def process_csv_files():
    """
    Process all CSV files in the current directory.
    For each CSV file, extract:
      - First Name from 3rd column (index 2)
      - Last Name from 4th column (index 3)
      - Email Address from 2nd column (index 1)
      - Roles: a list starting with the CSV filename (without extension)
    Merge duplicate records (by Email Address) and initialize extra columns.
    """
    records = {}
    
    for filename in os.listdir('.'):
        if filename.lower().endswith('.csv'):
            group_name = os.path.splitext(filename)[0]
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader, None)  # Skip header if present.
                for row in reader:
                    if len(row) >= 4:
                        first_name    = row[2]  # from 3rd column
                        last_name     = row[3]  # from 4th column
                        email_address = row[1]  # from 2nd column
                        
                        if email_address in records:
                            # Append CSV filename as role if not already present.
                            if group_name not in records[email_address]["Roles"]:
                                records[email_address]["Roles"].append(group_name)
                        else:
                            records[email_address] = {
                                "First Name": first_name,
                                "Last Name": last_name,
                                "Email Address": email_address,
                                "Roles": [group_name],
                                # Extra columns initialized to empty strings.
                                "DPE License Country": "",
                                "Country": "",
                                "Role2": "",
                                "Last Login Date": "",
                                "RITM#": "",
                                "Access Given": "",
                                "Date": ""
                            }
                    else:
                        print(f"Skipping incomplete row in {filename}: {row}")
    return list(records.values())

def update_table_with_excel(table, excel_filename):
    """
    Update records from ritm.xlsx.
    For each row (expected to have 12 columns), match based on the 4th column (index 3, email).
    Update fields as follows:
      - Base value from column 1 (index 0) after removing "PwC " (case-insensitive).
      - If new Role2 (column 5, index 4) contains "DPE License Country" (case-insensitive),
          then set DPE License Country to "Global" and do not update Role2/Access Given.
      - Otherwise:
            * For DPE License Country and Country:
                - If the record’s current DPE License Country and Country differ,
                  update only Country with the base value.
                - Otherwise, update both with the base value.
            * For Role2 (column 5) and RITM# (column 7); if a value already exists, append
              the new value (separated by ", "), otherwise simply assign it.
            * Then set Access Given equal to Role2.
      - Update Last Login Date (column 6, index 5) by simply taking the new value.
      - For Date (column 10, index 9, assumed dd/mm/yyyy), keep the more recent date.
    Also, count and print emails updated multiple times.
    """
    records = {record["Email Address"]: record for record in table}
    update_count = {}
    
    try:
        df = pd.read_excel(excel_filename, header=None)
    except Exception as e:
        print(f"Error reading {excel_filename}: {e}")
        return table
    
    for i, row in df.iterrows():
        email = row[3]  # Email from 4th column.
        if email in records:
            update_count[email] = update_count.get(email, 0) + 1
            rec = records[email]
            
            # Process base value from column 1 (index 0)
            base_value = row[0]
            if isinstance(base_value, str):
                base_value = re.sub(r'(?i)^pwc\s+', '', base_value)
            
            new_role2 = str(row[4]) if pd.notna(row[4]) else ""
            new_ritm = str(row[6]) if pd.notna(row[6]) else ""
            
            if "dpe license country" in new_role2.lower():
                rec["DPE License Country"] = "Global"
                # Skip updates for Role2 and Access Given.
            else:
                # Update DPE License Country and Country:
                # If current DPE License Country and Country are different, update only Country.
                if rec["DPE License Country"].strip() != rec["Country"].strip():
                    rec["Country"] = base_value
                else:
                    rec["DPE License Country"] = base_value
                    rec["Country"] = base_value
                
                # Update Role2: if already non-empty, append.
                if rec["Role2"]:
                    rec["Role2"] = f"{rec['Role2']}, {new_role2}" if new_role2 else rec["Role2"]
                else:
                    rec["Role2"] = new_role2
                
                # Update RITM# similarly: if non-empty, append new_ritm.
                if rec["RITM#"]:
                    rec["RITM#"] = f"{rec['RITM#']}, {new_ritm}" if new_ritm else rec["RITM#"]
                else:
                    rec["RITM#"] = new_ritm
                    
                # Set Access Given equal to Role2.
                rec["Access Given"] = rec["Role2"]
            
            # Update Last Login Date directly:
            if pd.notna(row[5]):
                rec["Last Login Date"] = row[5]
            
            # Update Date (column 10, index 9) with dd/mm/yyyy format.
            new_date_str = str(row[9]) if pd.notna(row[9]) else ""
            try:
                new_date = pd.to_datetime(new_date_str, format="%d/%m/%Y", errors='coerce')
            except Exception:
                new_date = pd.NaT
            existing_date_str = rec["Date"].strip() if isinstance(rec["Date"], str) else ""
            try:
                existing_date = pd.to_datetime(existing_date_str, format="%d/%m/%Y", errors='coerce') if existing_date_str else pd.NaT
            except Exception:
                existing_date = pd.NaT
            if pd.notna(new_date):
                if pd.isna(existing_date) or new_date > existing_date:
                    rec["Date"] = new_date_str

    for email, count in update_count.items():
        if count > 1:
            print(f"{email} was updated {count} times.")
    return list(records.values())

def update_table_with_updated_excel(table, updated_excel_filename):
    """
    Update the table using the updated.xlsx file.
    For each row in updated.xlsx:
      - Match records based on the email; the email is in the 5th column (index 4).
      - For a match:
          1. RITM#: Check value from column 8 (index 7). If it is not already present in rec["RITM#"]
             (split by comma and stripped), then append it.
          2. Last Login Date: Read the value from column 7 (index 6) which is in the ISO format
             ("2024-05-16T12:21:44.948Z"). Parse it and compare with existing rec["Last Login Date"] (if any).
             Then store the more recent value.
          3. DPE License Country: Read from column 1 (index 0). If its value is not already in rec["DPE License Country"]
             (split by comma and stripped), then append it.
             However, if before update the rec’s DPE License Country and Country were different and after appending they would become equal,
             then skip updating DPE License Country.
          4. Country: Read from column 2 (index 1); if not already present in rec["Country"], then append it.
    """
    records = {record["Email Address"]: record for record in table}
    
    try:
        df = pd.read_excel(updated_excel_filename, header=None)
    except Exception as e:
        print(f"Error reading {updated_excel_filename}: {e}")
        return table
    
    for i, row in df.iterrows():
        # Email (5th column, index 4).
        email = row[4]
        if email in records:
            rec = records[email]
            
            # 1. RITM#: update from column 8 (index 7).
            new_ritm = str(row[7]) if pd.notna(row[7]) else ""
            if new_ritm:
                # Check if new_ritm is already present in rec["RITM#"]
                current_ritm_list = [s.strip() for s in rec["RITM#"].split(",")] if rec["RITM#"] else []
                if new_ritm not in current_ritm_list:
                    if rec["RITM#"]:
                        rec["RITM#"] = f"{rec['RITM#']}, {new_ritm}"
                    else:
                        rec["RITM#"] = new_ritm
            
            # 2. Last Login Date from column 7 (index 6), in ISO format.
            new_last_login_iso = str(row[6]) if pd.notna(row[6]) else ""
            try:
                new_last_login = pd.to_datetime(new_last_login_iso, utc=True, errors='coerce')
            except Exception:
                new_last_login = pd.NaT
            try:
                existing_last_login = pd.to_datetime(rec["Last Login Date"], utc=True, errors='coerce')
            except Exception:
                existing_last_login = pd.NaT
            if pd.notna(new_last_login):
                if pd.isna(existing_last_login) or new_last_login > existing_last_login:
                    # Store back the ISO string. (Or you could format it as desired.)
                    rec["Last Login Date"] = new_last_login_iso
            
            # 3. DPE License Country update from column 1 (index 0).
            new_dpe = str(row[0]) if pd.notna(row[0]) else ""
            if new_dpe:
                current_dpe_list = [s.strip() for s in rec["DPE License Country"].split(",")] if rec["DPE License Country"] else []
                if new_dpe not in current_dpe_list:
                    # Determine if appending would make DPE License Country equal Country.
                    new_dpe_appended = (rec["DPE License Country"] + ", " + new_dpe) if rec["DPE License Country"] else new_dpe
                    # Split both updated DPE License Country and Country into lists for comparison.
                    dpe_updated = sorted([s.strip() for s in new_dpe_appended.split(",") if s.strip()])
                    country_updated = sorted([s.strip() for s in rec["Country"].split(",") if s.strip()])
                    # If they would become the same, skip updating DPE License Country.
                    if dpe_updated != country_updated:
                        rec["DPE License Country"] = new_dpe_appended
            
            # 4. Country update from column 2 (index 1).
            new_country = str(row[1]) if pd.notna(row[1]) else ""
            if new_country:
                current_country_list = [s.strip() for s in rec["Country"].split(",")] if rec["Country"] else []
                if new_country not in current_country_list:
                    if rec["Country"]:
                        rec["Country"] = f"{rec['Country']}, {new_country}"
                    else:
                        rec["Country"] = new_country
                    
    return list(records.values())

def count_rows_with_multiple_roles(table):
    """Count how many records have more than one role."""
    return sum(1 for row in table if len(row.get("Roles", [])) > 1)

def write_to_excel(table, excel_filename):
    """Write the table (a list of dicts) into an Excel file."""
    df = pd.DataFrame(table)
    # Convert the Roles list to a comma-separated string.
    df["Roles"] = df["Roles"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
    df.to_excel(excel_filename, index=False)
    print(f"Data successfully written to {excel_filename}")

if __name__ == "__main__":
    # Step 1: Process CSV files.
    table = process_csv_files()
    multi_role_count = count_rows_with_multiple_roles(table)
    print("Number of rows with more than 1 role:", multi_role_count)
    
    # Step 2: Update the table using ritm.xlsx.
    ritm_excel = "ritm.xlsx"
    table = update_table_with_excel(table, ritm_excel)
    
    # Step 3: Update the table with updated.xlsx.
    updated_excel = "updated.xlsx"
    table = update_table_with_updated_excel(table, updated_excel)
    
    # Optional: Create a new DataFrame from the updated table.
    updated_df = pd.DataFrame(table)
    
    # Step 4: Write the final table to "user report.xlsx".
    output_excel = "user report.xlsx"
    write_to_excel(table, output_excel)
