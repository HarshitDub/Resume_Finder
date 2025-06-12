# emailer.py

import smtplib, ssl
from email.message import EmailMessage
import boto3
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# ---- Load email credentials from environment ----
EMAIL_SENDER = os.getenv("GMAIL_USER")
EMAIL_PASS = os.getenv("GMAIL_PASS")

AWS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SES_SENDER = os.getenv("SES_SENDER")

def send_email_gmail(receiver, subject, body, attachment_path):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = receiver
        msg.set_content(body)

        # Attach file
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = Path(attachment_path).name
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

        # Send using Gmail SMTP
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASS)
            smtp.send_message(msg)
        print(f"✅ Email sent to {receiver} via Gmail")
        return True
    except Exception as e:
        print(f"❌ Gmail email failed: {e}")
        return False


def send_email_ses(receiver, subject, body, attachment_path):
    try:
        client = boto3.client(
            "ses",
            aws_access_key_id=AWS_KEY,
            aws_secret_access_key=AWS_SECRET,
            region_name=AWS_REGION
        )

        # Read file content
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = Path(attachment_path).name

        # Construct raw email
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = SES_SENDER
        msg["To"] = receiver
        msg.set_content(body)
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

        # Send raw email via SES
        client.send_raw_email(
            Source=SES_SENDER,
            Destinations=[receiver],
            RawMessage={"Data": msg.as_bytes()}
        )
        print(f"✅ Email sent to {receiver} via AWS SES")
        return True
    except Exception as e:
        print(f"❌ SES email failed: {e}")
        return False
