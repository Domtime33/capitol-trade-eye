import streamlit as st
import pandas as pd
import plotly.express as px
from trade_scraper import get_all_trade_data, get_cached_data, save_to_cache
from utils import extract_tickers_from_disclosures, generate_recommendations
from datetime import datetime, timedelta

st.set_page_config(page_title="Capitol Trade AI", layout="wide")
st.title("📈 Capitol Trade AI")
st.caption("Get stock picks based on real-time congressional trades.")

# Try fetching new trade data, fallback to cache if unavailable
try:
    data = get_all_trade_data()
    if data.empty:
        st.warning("No recent trade data available right now. Please try again later.")
        data = get_cached_data()
    else:
        save_to_cache(data)
except Exception as e:
    st.error(f"Error fetching data: {e}")
    data = get_cached_data()

# If still empty, show fallback warning
if data.empty:
    st.warning("⚠ No trade data available from cache or live source.")
else:
    # Filter data for last 7 days
    st.subheader("🗓️ Trades in the Last 7 Days")
    one_week_ago = datetime.now() - timedelta(days=7)
    recent_trades = data[data['Transaction Date'] >= one_week_ago.strftime('%Y-%m-%d')]

    st.dataframe(
        recent_trades.sort_values(by='Transaction Date', ascending=False),
        use_container_width=True
    )

    # Extract tickers
    tickers = extract_tickers_from_disclosures(recent_trades)

    if tickers:
        st.subheader("📊 Mentioned Tickers")
        st.write(', '.join(tickers))

        # Generate recommendations
        recommendations = generate_recommendations(tickers, recent_trades)
        if not recommendations.empty:
            st.subheader("🔍 Trade-Based Stock Recommendations")
            st.dataframe(recommendations, use_container_width=True)
        else:
            st.info("No strong patterns detected in trade data.")
    else:
        st.info("No tickers extracted from trades in the past 7 days.")
