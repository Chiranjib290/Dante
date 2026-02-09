import requests
import xlsxwriter
import datetime
import Adder

# Replace with secure credential handling in production
uname = "debolina.b.dutta@in.pwc.com"
passwd = "Change@123456"
BASE_URL = "https://dpe.pwc.com"

date = datetime.date.today()
filename = f'obscene_data_{date}.xlsx'
print(f"Filename : {filename}")

workbook = xlsxwriter.Workbook(filename)


def obscene():
    worksheet = workbook.add_worksheet("Obscene Check")
    get_url = (
        f'{BASE_URL}/libs/cq/workflow/content/inbox/list.json'
        '?filter-itemType=workitem&filter-model=/var/workflow/models/pwc-form-submission-obscene-check-v2'
    )

    resp = requests.get(get_url, auth=(uname, passwd))
    resp.raise_for_status()
    data = resp.json()
    print("Inbox response:", data)

    data_items = data.get('items', [])
    payloads = [item.get('payloadPath') for item in data_items if 'payloadPath' in item]

    # Header
    worksheet.write(0, 0, "Payload")
    worksheet.write(0, 1, "Banned Words(if present)")
    worksheet.write(0, 2, "Status")

    # Load banned words once and normalize (do not mutate original list)
    bw_resp = requests.get(f'{BASE_URL}/content/pwc/global/referencedata/bannedWords.json',
                           auth=(uname, passwd))
    bw_resp.raise_for_status()
    data_bannedwords = bw_resp.json()
    bannedwords_master = [w.strip() for w in data_bannedwords.get('bannedWords', []) if w is not None]

    # Adder.adder assumed to be iterable (list/set) of words to treat specially
    adder = getattr(Adder, 'adder', []) or []

    for idx, url in enumerate(payloads, start=1):
        try:
            row = idx
            nodata = ""
            # Make a fresh copy of banned words for this payload so we can remove territory-specific words
            bannedwords = bannedwords_master.copy()

            # Fetch payload JSON
            get_url = f'{BASE_URL}{url}.json'
            r = requests.get(get_url, auth=(uname, passwd))
            if r.status_code != 200:
                print(f"Skipping {url}: HTTP {r.status_code}")
                worksheet.write(row, 0, url)
                worksheet.write(row, 1, nodata)
                worksheet.write(row, 2, f"Failed to fetch payload: HTTP {r.status_code}")
                continue

            data2 = r.json()
            data1 = str(data2)

            # Build search string depending on form type
            searchstring = ""
            if data2.get('formType') == 'contactUs':
                company = data2.get('company', '')
                email = data2.get('email', '')
                fullName = data2.get('fullName', '')
                queryDetails = data2.get('queryDetails', '')
                querysubject = data2.get('querysubject', '')
                job_role = data2.get('job_role', '')
                telephone = data2.get('telephone', '')
                searchstring = ' '.join([company, email, fullName, queryDetails, querysubject, job_role, telephone]).strip()
            elif data2.get("pwcFormFieldOrder"):
                formfields = data2.get('pwcFormFieldOrder', '')
                formfieldslist = [f.strip() for f in formfields.split(",") if f.strip()]
                parts = [str(data2.get(field, '')) for field in formfieldslist]
                searchstring = ' '.join(parts).strip()
            elif 'g-recaptcha-response' in data2:
                grecaptcharesponse = data2.get('g-recaptcha-response', '')
                refined_data1 = data1.replace(str(grecaptcharesponse), '')
                searchstring = refined_data1
            else:
                searchstring = data1

            # Territory-specific removals (operate on local copy)
            if "/content/pwc/in/en" in url and 'sikkim' in bannedwords:
                bannedwords.remove("sikkim")
            if "/content/pwc/cn/" in url and 'poon' in bannedwords:
                bannedwords.remove("poon")
            if "/content/pwc/hk/" in url and 'poon' in bannedwords:
                bannedwords.remove("poon")

            # Lowercase once for efficiency
            search_lower = searchstring.lower()

            found_word = None
            # Initialize flag: assume not found
            b = 1

            for x in bannedwords:
                x1 = x.replace('\n', '').strip()
                # If x1 is in adder, require word boundaries by surrounding with spaces
                if x1 in adder:
                    # check with spaces to reduce false positives
                    pattern = f' {x1} '
                    if pattern.lower() in search_lower:
                        found_word = x
                        b = 0
                        break
                else:
                    # simple substring match (case-insensitive)
                    if x1 and x1.lower() in search_lower:
                        found_word = x
                        b = 0
                        break

            if b == 0 and found_word:
                print("Writing data for", url, found_word)
                worksheet.write(row, 0, url)
                worksheet.write(row, 1, str(found_word))
                worksheet.write(row, 2, "Banned Word Present")
            else:
                print("Writing data for", url, "no banned words")
                worksheet.write(row, 0, url)
                worksheet.write(row, 1, nodata)
                worksheet.write(row, 2, "Banned Words were not Present")

        except Exception as e:
            # Log and continue with next payload
            print("Exception processing", url, ":", e)
            worksheet.write(idx, 0, url)
            worksheet.write(idx, 1, "")
            worksheet.write(idx, 2, f"Error: {e}")


def mx_lookup():
    worksheet = workbook.add_worksheet("MX Lookup")
    get_url = (
        f'{BASE_URL}/libs/cq/workflow/content/inbox/list.json'
        '?filter-itemType=workitem&filter-model=/var/workflow/models/pwc-form-submission-mx-lookup-check-v2'
    )
    r = requests.get(get_url, auth=(uname, passwd))
    r.raise_for_status()
    data = r.json()
    print("MX inbox response:", data)

    worksheet.write(0, 0, "Payload")
    worksheet.write(0, 1, "Email")
    row = 0

    data_items = data.get('items', [])
    for each in data_items:
        row += 1
        pay_load = each.get('payloadPath', '')
        # Use .json endpoint to get structured data
        url = f'{BASE_URL}{pay_load}.json'
        email = ""
        try:
            r = requests.get(url, auth=(uname, passwd))
            if r.status_code == 200:
                data2 = r.json()
                mail1 = data2.get("E-mailadres", "")
                mail2 = data2.get("email", "")
                if mail1:
                    email = mail1
                elif mail2:
                    email = mail2
        except Exception as e:
            print("Error fetching MX payload", pay_load, ":", e)

        worksheet.write(row, 0, pay_load)
        worksheet.write(row, 1, email)


if __name__ == "__main__":
    try:
        obscene()
        mx_lookup()
    finally:
        workbook.close()
        print("Workbook closed:", filename)
