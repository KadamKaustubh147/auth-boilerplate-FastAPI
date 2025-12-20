import smtplib
from email.message import EmailMessage
from app.core.config import settings

def send_verification_email(email: str, token: str):
    verify_url = f"{settings.FRONTEND_ORIGIN}/verify-email/{token}"

    msg = EmailMessage()
    msg["Subject"] = "Verify Your Email"
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = email
    msg.set_content(f"Click to verify:\n\n{verify_url}")

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        server.send_message(msg)
