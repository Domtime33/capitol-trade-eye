import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Capitol Trade Eye", layout="wide")

st.markdown("<h1 style='text-align: center;'>📊 Capitol Trade Eye</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Live updates on U.S. Congress stock trades from <a href='https://www.quiverquant.com/' target='_blank'>QuiverQuant</a></p>", unsafe_allow_html=True)

API_URL = "https://api.quiverquant.com/beta/historical/congresstrading"
HEADERS = {"accept": "application/json"}

def fetch_congress_trades():
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch data from QuiverQuant API.\n\nError: {str(e)}")
        return []

data = fetch_congress_trades()

if not data:
    st.warning("⚠️ No recent trade data available right now. Please try again later.")
else:
    df = pd.DataFrame(data)
    df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])

    # Display summary
    st.subheader("🗓️ Latest Trades")
    st.dataframe(df.sort_values("TransactionDate", ascending=False).head(15), use_container_width=True)

    # Plot trade volume by ticker
    fig = px.histogram(df, x="Ticker", title="Most Traded Stocks by Congress", nbins=50)
    st.plotly_chart(fig, use_container_width=True)
