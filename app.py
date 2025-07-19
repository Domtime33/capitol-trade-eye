import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

# ---- CONFIG ----
API_URL = "https://api.quiverquant.com/beta/live/congresstrading"
API_KEY = "demo"  # Public demo key — limited access

# ---- LOAD DATA ----
@st.cache_data(ttl=3600)
def load_trade_data():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(API_URL, headers=headers)

    if response.status_code != 200:
        st.error("Failed to fetch data from QuiverQuant API.")
        return pd.DataFrame()

    data = response.json()
    df = pd.DataFrame(data)

    if df.empty:
        return df

    df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
    df['Amount'] = df['Range'].fillna("Unknown")
    return df

# ---- UI ----
st.set_page_config(page_title="Capitol Trade Eye", layout="wide")
st.title("📊 Capitol Trade Eye")
st.markdown("Live updates on U.S. Congress stock trades from [QuiverQuant](https://www.quiverquant.com/)")

df = load_trade_data()

if df.empty:
    st.warning("No recent trade data available right now. Please try again later.")
    st.stop()

# ---- FILTERS ----
col1, col2 = st.columns(2)
with col1:
    selected_person = st.selectbox("Filter by Congressperson", ["All"] + sorted(df['Representative'].unique()))
with col2:
    selected_ticker = st.selectbox("Filter by Ticker", ["All"] + sorted(df['Ticker'].dropna().unique()))

filtered_df = df.copy()
if selected_person != "All":
    filtered_df = filtered_df[filtered_df['Representative'] == selected_person]
if selected_ticker != "All":
    filtered_df = filtered_df[filtered_df['Ticker'] == selected_ticker]

# ---- PLOT ----
st.subheader("Trade Timeline")
fig = px.scatter(
    filtered_df,
    x="TransactionDate",
    y="Ticker",
    color="Representative",
    hover_data=["Amount", "Transaction", "Representative"],
    title="Congressional Trades Over Time"
)
st.plotly_chart(fig, use_container_width=True)

# ---- TABLE ----
st.subheader("Trade Details")
st.dataframe(filtered_df.sort_values("TransactionDate", ascending=False), use_container_width=True)
