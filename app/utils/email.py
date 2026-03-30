# utils/email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.config import settings


def send_email(to: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.starttls()
        server.login(
            settings.EMAIL_FROM,
            settings.EMAIL_PASSWORD
        )
        server.send_message(msg)
        server.quit()

        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Email error:", str(e))


def send_otp_email(email: str, otp: str):
    subject = "Your Login OTP"
    body = f"""
Hello,

Your OTP for login is: {otp}

⏱ This OTP is valid for 5 minutes.
⚠ Do not share this OTP with anyone.

Thanks,
Security Team
"""
    send_email(email, subject, body)