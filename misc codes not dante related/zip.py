import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# 1. Email setup
sender_email = "chiranjib290@gmail.com"
password     = "gmjp gkyo ebys qttn"   # App password

print("hellp")

# 2. Recipient
recipients = ["chiranjibdarktitan@gmail.com"]

subject = "ZIP File Delivery"
body    = "Please find the ZIP file attached."

# 3. ZIP file path
file_name = "zup.tar"
file_path = os.path.join(os.getcwd(), file_name)  # or any absolute path

# 4. Construct the email
message = MIMEMultipart()
message["From"] = sender_email
message["To"]   = ", ".join(recipients)
message["Subject"] = subject

# 5. Attach body text
message.attach(MIMEText(body, "plain"))

# 6. Attach ZIP file
with open(file_path, "rb") as attachment:
    part = MIMEBase("application", "x-tar")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={file_name}"
    )
    message.attach(part)


# 7. Send email
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, recipients, message.as_string())
    server.quit()
    print("Email sent to:", recipients)
except Exception as e:
    print("Failed to send email:", e)
