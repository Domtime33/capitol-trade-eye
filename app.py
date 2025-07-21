import streamlit as st
import pandas as pd
import plotly.express as px
from trade_scraper import get_all_trade_data, get_cached_data, save_to_cache
from utils import extract_tickers_from_disclosures, generate_recommendations
from datetime import datetime, timedelta

st.set_page_config(page_title="Capitol Trade AI", layout="wide")
st.title("📈 Capitol Trade AI")
st.caption("Get stock picks based on real-time congressional trades")

# Load trade data
try:
    data = get_all_trade_data()
    if data.empty:
        st.warning("No recent trade data available right now. Please try again later.")
    else:
        # Cache for daily view
        save_to_cache(data)
except Exception as e:
    st.error(f"Error fetching data: {e}")
    data = get_cached_data()
    if data.empty:
        st.warning("⚠ No trade data available.")

# Show 7-day snapshot
if not data.empty:
    st.subheader("🗓️ Trades in the Last 7 Days")
    one_week_ago = datetime.now() - timedelta(days=7)
    recent_trades = data[data['Transaction Date'] >= one_week_ago.strftime('%Y-%m-%d')]

    st.dataframe(recent_trades.sort_values(by='Transaction Date', ascending=False))

    tickers = extract_tickers_from_disclosures(recent_trades)
    if tickers:
        st.subheader("📊 Mentioned Tickers")
        st.write(', '.join(tickers))

        recommendations = generate_recommendations(tickers, recent_trades)
        if not recommendations.empty:
            st.subheader("🔍 Trade-Based Stock Recommendations")
            st.dataframe(recommendations)
        else:
            st.info("No strong patterns detected in current trade volume.")
    else:
        st.info("No tickers extracted from trades in past 7 days.")
