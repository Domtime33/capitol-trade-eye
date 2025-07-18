import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="Capitol Trade Eye", layout="wide")
st.title("👁️ Capitol Trade Eye – Live Congressional Stock Trades")

# --- Scrape most recent trades from CapitolTrades.com ---
@st.cache_data(ttl=3600)
def scrape_recent_trades():
    url = "https://www.capitoltrades.com/trades"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.select("div.sc-ikJyIC")  # Each trade row
    data = []

    for row in rows:
        try:
            name = row.select_one("a.sc-himrzO").text.strip()
            ticker = row.select_one("a.sc-himrzO + span").text.strip().replace("(", "").replace(")", "")
            transaction = row.find("span", string=lambda t: t and "Purchase" in t or "Sale" in t).text.strip()
            date_text = row.find("span", string=lambda t: t and "Reported" in t).text.replace("Reported", "").strip()
            reported_date = datetime.strptime(date_text, "%b %d, %Y")
            party = row.select_one("div.sc-jUosCB").text.strip()

            data.append({
                "Name": name,
                "Ticker": ticker,
                "Transaction": transaction,
                "Reported Date": reported_date,
                "Party": party
            })
        except:
            continue

    return pd.DataFrame(data)

df = scrape_recent_trades()

if df.empty:
    st.warning("No recent trade data available right now. Please try again later.")
    st.stop()

# --- Sidebar filters ---
with st.sidebar:
    st.header("🔍 Filter Options")
    tickers = sorted(df["Ticker"].unique())
    selected_tickers = st.multiselect("Filter by Ticker", tickers, default=tickers)
    parties = sorted(df["Party"].unique())
    selected_parties = st.multiselect("Filter by Party", parties, default=parties)

# --- Filtered Data ---
filtered_df = df[
    (df["Ticker"].isin(selected_tickers)) &
    (df["Party"].isin(selected_parties))
]

st.markdown("### 📈 Latest Trades")
st.dataframe(filtered_df, use_container_width=True)

# --- Plotly Chart ---
fig = px.histogram(
    filtered_df,
    x="Ticker",
    color="Transaction",
    barmode="group",
    title="🗳️ Trades by Ticker & Type",
)
st.plotly_chart(fig, use_container_width=True)
