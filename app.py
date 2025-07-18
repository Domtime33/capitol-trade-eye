import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime

st.set_page_config(page_title="Capitol Trade AI", layout="wide")

# --- HEADER ---
st.title("🏛️ Capitol Trade AI")
st.caption("Track U.S. politician stock trades and simulate a $10,000 mirror strategy.")

# --- LOAD DATA ---
@st.cache_data
def load_trade_data():
    data = pd.read_csv("data/congress_trades.csv")
    data['TransactionDate'] = pd.to_datetime(data['TransactionDate'])
    return data

df = load_trade_data()

# --- USER INPUTS ---
politicians = df['Representative'].dropna().unique().tolist()
selected = st.multiselect("Select Politicians", politicians, default=politicians[:3])
days = st.radio("Trend Chart", ["1 Day", "30 Days", "6 Months"], horizontal=True)
fund = st.slider("Mirror Strategy Investment Amount", 1000, 10000, 10000, step=500)

# --- FILTERED DATA ---
filtered = df[df['Representative'].isin(selected)].copy()
filtered = filtered.sort_values(by="TransactionDate", ascending=False)

# --- ALLOCATION CALCULATION ---
num_trades = filtered.shape[0]
filtered["Allocation ($)"] = (fund / num_trades).round(2) if num_trades else 0

# --- DISPLAY DATA ---
st.subheader("📊 Trade Table")
st.dataframe(
    filtered[["Representative", "TransactionDate", "Ticker", "Transaction", "Amount", "Allocation ($)"]],
    use_container_width=True
)

# --- STOCK TREND CHARTS ---
st.subheader("📈 Stock Trend Viewer")

for ticker in filtered['Ticker'].unique():
    if pd.isna(ticker) or ticker.strip() == "":
        continue

    stock = yf.Ticker(ticker.strip())
    period = {"1 Day": "1d", "30 Days": "1mo", "6 Months": "6mo"}[days]

    try:
        hist = stock.history(period=period)
        if hist.empty:
            continue

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name=ticker.upper()))
        fig.update_layout(
            title=f"{ticker.upper()} - {days} Trend",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not retrieve data for {ticker}: {e}")

# --- EMAIL TEST BUTTON ---
with st.expander("📧 Email Test (Admin Only)"):
    recipient = st.text_input("Test Recipient Email")
    if st.button("Send Test Email"):
        if recipient:
            try:
                def send_email(subject, content, recipient_email):
                    message = Mail(
                        from_email=st.secrets["sendgrid"]["sender_email"],
                        to_emails=recipient_email,
                        subject=subject,
                        html_content=content
                    )
                    sg = SendGridAPIClient(st.secrets["sendgrid"]["api_key"])
                    return sg.send(message)

                response = send_email("Test from Capitol Trade AI", "This is a test email.", recipient)
                st.success("Test email sent successfully!")
            except Exception as e:
                st.error(f"Email failed: {e}")
        else:
            st.warning("Enter a recipient email.")

# --- FOOTER ---
st.markdown("---")
st.caption("© 2025 Capitol Trade AI — Built for transparency.")
