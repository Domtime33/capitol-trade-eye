from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import SENDGRID_API_KEY, EMAIL_TO, EMAIL_FROM
import pandas as pd

def send_email(recommendations: pd.DataFrame):
    if recommendations.empty:
        return

    html_content = recommendations.to_html(index=False)

    message = Mail(
        from_email=EMAIL_FROM,
        to_emails=EMAIL_TO,
        subject="📈 Capitol Trade AI – Today's Stock Picks",
        html_content=f"""
        <p>Here are your trade-based picks from Congress in the last 7 days:</p>
        {html_content}
        <p>-- Capitol Trade AI</p>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent: {response.status_code}")
    except Exception as e:
        print(f"Email send failed: {e}")
