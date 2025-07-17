import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Capitol Trade AI", layout="wide")

st.title("📈 Capitol Trade AI")
st.subheader("Tracking Stock Moves by U.S. Politicians")

# Simulated daily email summary
today = datetime.date.today().strftime("%B %d, %Y")

st.markdown(f"### 📬 Daily Summary for {today}")

data = {
    "Name": ["Nancy Pelosi", "Josh Hawley", "Dan Crenshaw"],
    "Stock": ["NVDA", "AAPL", "MSFT"],
    "Action": ["Buy", "Sell", "Buy"],
    "Amount": ["$250,000", "$100,000", "$150,000"],
    "Date": [today, today, today]
}

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)

st.markdown("---")
st.markdown("📧 You will receive email alerts as new trades are published.")

st.caption("Data provided by Capitol Trade AI • Not financial advice.")
import streamlit as st
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(subject, content, to_email):
    message = Mail(
        from_email=st.secrets["sendgrid"]["sender_email"],
        to_emails=to_email,
        subject=subject,
        plain_text_content=content
    )
    try:
        sg = SendGridAPIClient(st.secrets["sendgrid"]["api_key"])
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        return str(e)

# Streamlit Test Button
st.header("📧 SendGrid Email Test")

recipient = st.text_input("Enter recipient email")
if st.button("Send Test Email"):
    if recipient:
        status = send_email("Test from Capitol Trade AI", "This is a test email.", recipient)
        st.success(f"Email sent! Status: {status}")
    else:
        st.warning("Please enter a recipient email.")
