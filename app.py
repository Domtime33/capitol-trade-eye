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
