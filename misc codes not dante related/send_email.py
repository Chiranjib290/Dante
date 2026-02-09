import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# 1. Email setup
sender_email = "chiranjib290@gmail.com"
password     = "gmjp gkyo ebys qttn"

# 2. Define recipients
recipients = [
    "chiranjib.bhattacharyya@pwc.com",
    "riddhi.chowdhury@pwc.com",
    "mehena.majumdar@pwc.com",
    "vasupalli.suraj@pwc.com",
    "saahil.sankar@pwc.com"
]

subject = "Subject of the Email"
body    = "Body of the email with attachment"

# 3. Locate the file to attach
file_name = os.getenv('EXCEL_FILE_NAME')
build_dir = os.getenv('BUILD_ARTIFACT_STAGING_DIRECTORY')
file_path = os.path.join(build_dir, file_name)

# 4. Construct the email
message = MIMEMultipart()
message["From"] = sender_email
message["To"]   = ", ".join(recipients)
message["Subject"] = subject

# 5. Attach the body text
message.attach(MIMEText(body, "plain"))

# 6. Attach the Excel file
with open(file_path, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={file_name}"
    )
    message.attach(part)

# 7. Send the email
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)

    # Note: sendmail() accepts a list of recipients
    server.sendmail(sender_email, recipients, message.as_string())
    server.quit()
    print("Email sent to:", recipients)
except Exception as e:
    print("Failed to send email:", e)