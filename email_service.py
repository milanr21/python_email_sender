import os
import smtplib
from email.message import EmailMessage


def send_email(recipient: str, subject:str,sender_email: str, body:str)-> None:
    sender = os.getenv("SMTP_SENDER")
    password = os.getenv("SMTP_PASSWORD")
    smtp_sever = os.getenv("SMTP_SERVER")
    smtp_port =  int(os.getenv("SMTP_PORT", "587"))
    
    if not all([sender, password, smtp_sever]):
        raise ValueError("Missing SMTP configuration")
    
    msg = EmailMessage()
    msg['From'] = sender
    msg["To"] = recipient
    msg["Cc"] = sender_email
    msg["Subject"] = subject
    msg.set_content(body)
    
    with smtplib.SMTP(smtp_sever, smtp_port, timeout=15) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)