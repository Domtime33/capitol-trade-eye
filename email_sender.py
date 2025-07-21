import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, body):
    from_email = "domsoccerplayer@gmail.com"
    smtp_server = "smtp.sendgrid.net"
    smtp_port = 587
    smtp_username = "apikey"
    smtp_password = "YOUR_SENDGRID_API_KEY"  # 🔐 Replace with actual SendGrid API key

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
