import sendgrid
from sendgrid.helpers.mail import Mail
import pandas as pd
import os

def send_email_report(df):
    if df.empty:
        return

    content = "📈 Daily Capitol Trade Picks\n\n"
    for _, row in df.iterrows():
        content += f"{row['Ticker']}: Buy {row['Buy Qty']} shares @ ${row['Price']} = ${row['Investment']}\n"

    message = Mail(
        from_email="capitol@yourapp.com",
        to_emails="domsoccerplayer@gmail.com",
        subject="Capitol Trade AI – Daily Picks",
        plain_text_content=content
    )

    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"Email failed: {e}")
