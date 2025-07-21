import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from trade_scraper import get_all_trade_data, get_cached_data, save_to_cache
from utils import extract_tickers_from_disclosures, generate_recommendations
from emailer import send_email

st.set_page_config(page_title="Capitol Trade AI", layout="wide")
st.title("📈 Capitol Trade AI")
st.caption("Get stock picks based on real-time congressional trades")

# Load data
try:
    data = get_all_trade_data()
    save_to_cache(data)
except:
    data = get_cached_data()
    if data.empty:
        st.error("No trade data available.")
        st.stop()

# Filter past 7 days
one_week_ago = datetime.now() - timedelta(days=7)
recent_trades = data[data['Transaction Date'] >= one_week_ago]

st.subheader("🗓️ Trades in the Last 7 Days")
st.dataframe(recent_trades)

# Extract tickers
tickers = extract_tickers_from_disclosures(recent_trades)
if tickers:
    st.subheader("📊 Tickers Mentioned")
    st.write(", ".join(tickers))

    recommendations = generate_recommendations(tickers, recent_trades)

    if not recommendations.empty:
        st.subheader("✅ Buy Recommendations (Based on $10K virtual budget)")
        st.dataframe(recommendations)

        # Send Email on Page Load
        send_email(recommendations)
        st.success("✅ Daily email sent with recommendations.")
    else:
        st.info("No strong patterns to recommend.")
else:
    st.info("No tickers found in last 7 days.")
from email_sender import send_email_report

# Send once daily
if not data.empty and not recommendations.empty:
    send_email_report(recommendations)
