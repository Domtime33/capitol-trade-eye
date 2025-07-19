import streamlit as st
import requests
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import yfinance as yf
from collections import Counter
from io import StringIO

# ========== CONFIG ========== #
CACHE_FILE = "cache/congress_trades.json"
TODAY = datetime.utcnow().date()
ONE_WEEK_AGO = TODAY - timedelta(days=7)

st.set_page_config(page_title="Capitol Trade AI", layout="wide")

# ========== HELPERS ========== #

def fetch_data():
    """Scrape House and Senate trades"""
    try:
        house_url = "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json"
        senate_url = "https://senatestockwatcher.com/api/transactions"

        house_resp = requests.get(house_url, timeout=10)
        senate_resp = requests.get(senate_url, timeout=10)

        house_data = house_resp.json()
        senate_data = senate_resp.json()

        combined = []

        for entry in house_data:
            try:
                trade_date = datetime.strptime(entry["transaction_date"], "%Y-%m-%d").date()
                if trade_date >= ONE_WEEK_AGO:
                    combined.append({
                        "date": str(trade_date),
                        "chamber": "House",
                        "ticker": entry.get("ticker", ""),
                        "type": entry.get("type", ""),
                        "amount": entry.get("amount", ""),
                        "asset_description": entry.get("asset_description", "")
                    })
            except:
                continue

        for entry in senate_data.get("transactions", []):
            try:
                trade_date = datetime.strptime(entry["transaction_date"], "%Y-%m-%d").date()
                if trade_date >= ONE_WEEK_AGO:
                    combined.append({
                        "date": str(trade_date),
                        "chamber": "Senate",
                        "ticker": entry.get("ticker", ""),
                        "type": entry.get("type", ""),
                        "amount": entry.get("amount", ""),
                        "asset_description": entry.get("asset_description", "")
                    })
            except:
                continue

        return combined
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

def save_cache(data):
    os.makedirs("cache", exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return []

def get_top_tickers(trades):
    tickers = [t["ticker"] for t in trades if t["type"].lower() == "purchase" and t["ticker"] not in ["", "N/A", "na"]]
    top = Counter(tickers).most_common(10)
    return [t[0] for t in top]

def get_price_sparkline(ticker):
    try:
        df = yf.download(ticker, period="7d", interval="1d", progress=False)
        return df["Close"].tolist()
    except:
        return []

def generate_recommendations(tickers):
    data = []
    for t in tickers:
        sparkline = get_price_sparkline(t)
        if len(sparkline) > 1:
            trend = round((sparkline[-1] - sparkline[0]) / sparkline[0] * 100, 2)
        else:
            trend = 0.0
        data.append({
            "ticker": t,
            "trend_7d": f"{trend}%",
            "sparkline": sparkline
        })
    return data

# ========== LOAD DATA ========== #

with st.spinner("Loading Congressional trading data..."):
    trades = fetch_data()
    if trades:
        save_cache(trades)
    else:
        trades = load_cache()

# ========== UI ========== #

st.title("📈 Capitol Trade AI")
st.markdown("Get stock picks based on real-time congressional trades.")

if not trades:
    st.warning("⚠ No trade data available.")
    st.stop()

# 7-day snapshot
st.subheader("🗓 7-Day Snapshot of Congressional Trades")
df = pd.DataFrame(trades)
df = df[df["ticker"] != ""]  # Clean empty tickers
st.dataframe(df.sort_values("date", ascending=False), use_container_width=True)

# Top trades
top_tickers = get_top_tickers(trades)
st.subheader("🔥 Most Purchased Tickers by Politicians (Last 7 Days)")
st.write(", ".join(top_tickers))

# Recommendations
st.subheader("✅ Buy Recommendations Based on Trade Volume + Trend")

recommendations = generate_recommendations(top_tickers)

for rec in recommendations:
    st.markdown(f"**{rec['ticker']}** - 7d Trend: `{rec['trend_7d']}`")
    st.line_chart(rec["sparkline"])

# Placeholder: Email system will use this logic daily
email_output = StringIO()
email_output.write("📬 Capitol Trade AI – Daily Trade Summary\n\n")
email_output.write(f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}\n\n")
email_output.write("Top Trades:\n")
for rec in recommendations:
    email_output.write(f"- {rec['ticker']}: {rec['trend_7d']} trend (based on congressional buying)\n")

st.download_button("📤 Preview Daily Email Summary", email_output.getvalue(), file_name="daily_summary.txt")

# ========== END ========== #

