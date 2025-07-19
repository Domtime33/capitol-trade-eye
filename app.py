import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Capitol Trade Eye", page_icon="📊", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: white;'>Capitol Trade Eye</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center;'>Live updates on U.S. Congress stock trades from public disclosure sources.</p>",
    unsafe_allow_html=True,
)

@st.cache_data(ttl=3600)
def fetch_senate_data():
    try:
        url = "https://senatestockwatcher.com/api/transactions"
        response = requests.get(url)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return None
    except Exception as e:
        st.error(f"Error fetching Senate data: {e}")
        return None

df = fetch_senate_data()

if df is None or df.empty:
    st.error("No recent trade data available right now. Please try again later.")
else:
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df.sort_values("transaction_date", ascending=False, inplace=True)

    st.success(f"Showing {len(df)} recent Senate transactions.")
    st.dataframe(df[[
        "senator", "ticker", "type", "amount", "transaction_date", "asset_description"
    ]].rename(columns={
        "senator": "Senator",
        "ticker": "Ticker",
        "type": "Type",
        "amount": "Amount",
        "transaction_date": "Date",
        "asset_description": "Asset Description"
    }))

