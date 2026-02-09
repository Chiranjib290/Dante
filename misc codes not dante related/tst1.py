import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Email setup
sender_email = "chiranjib290@gmail.com"
receiver_email = "chiranjib.bhattacharyya@pwc.com"
password = "gmjp gkyo ebys qttn"
subject = "Subject of the Email"
body = "Body"
file_path = "obscene.xlsx"  # Path to your Excel file

# Creating the email content
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Attaching the body text to the email
message.attach(MIMEText(body, "plain"))

# Attaching the Excel file
attachment = open(file_path, "rb")
part = MIMEBase("application", "octet-stream")
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header("Content-Disposition", f"attachment; filename= {file_path.split('/')[-1]}")
message.attach(part)

# Sending the email
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)  # Using Gmail's SMTP server
    server.starttls()  # Securing the connection
    server.login(sender_email, password)
    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
