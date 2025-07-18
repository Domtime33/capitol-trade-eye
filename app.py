import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

st.set_page_config(page_title="Capitol Trade Eye", layout="wide")

# -----------------------------
# Scraper function using Selenium
# -----------------------------
@st.cache_data(ttl=3600)
def scrape_recent_trades():
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    driver.get("https://www.capitoltrades.com/trades")
    driver.implicitly_wait(10)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    rows = soup.select("div[class*=TradeRow__TradeRowWrapper]")
    data = []

    for row in rows:
        try:
            name = row.select_one("a[class*=Link__StyledLink]").text.strip()
            ticker = row.select_one("span[class*=TradeRow__Ticker]").text.strip()
            transaction = row.select_one("span[class*=TransactionType]").text.strip()
            date_text = row.select_one("span[class*=ReportedDate]").text.strip().replace("Reported", "").strip()
            reported_date = datetime.strptime(date_text, "%b %d, %Y")
            party = row.select_one("div[class*=TradeRow__MemberDetails]").text.strip().split("\n")[0]

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

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("📊 Capitol Trade Eye")
st.markdown("Live dashboard for real-time U.S. Congress stock trade disclosures.")

with st.spinner("🔍 Scraping latest trades..."):
    df = scrape_recent_trades()

if df.empty:
    st.error("❌ No recent trade data available. Please try again later.")
    st.stop()

# Date filter
min_date = df["Reported Date"].min()
max_date = df["Reported Date"].max()
start_date, end_date = st.date_input("Filter by reported date range:", [min_date, max_date])

filtered_df = df[(df["Reported Date"] >= pd.to_datetime(start_date)) &
                 (df["Reported Date"] <= pd.to_datetime(end_date))]

# Show trades
st.subheader("📋 Recent Trades")
st.dataframe(filtered_df.sort_values("Reported Date", ascending=False), use_container_width=True)

# Grouped summary
st.subheader("📈 Trade Volume by Ticker")
trade_counts = filtered_df["Ticker"].value_counts().reset_index()
trade_counts.columns = ["Ticker", "Number of Trades"]

fig = px.bar(trade_counts, x="Ticker", y="Number of Trades", title="Most Traded Stocks", text="Number of Trades")
st.plotly_chart(fig, use_container_width=True)

# Filter by politician
st.subheader("🧑‍⚖️ View by Member of Congress")
member_list = filtered_df["Name"].unique()
selected_member = st.selectbox("Select a member", sorted(member_list))

member_trades = filtered_df[filtered_df["Name"] == selected_member]
st.write(f"Trades by **{selected_member}**:")
st.dataframe(member_trades.sort_values("Reported Date", ascending=False), use_container_width=True)
