import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

def get_all_trade_data():
    # Example scraping from House stock watcher JSON
    url = "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json"
    r = requests.get(url)
    trades = r.json()
    df = pd.DataFrame(trades)
    df['Transaction Date'] = pd.to_datetime(df['transaction_date'])
    return df

def get_cached_data():
    try:
        return pd.read_csv("cached_data.csv", parse_dates=['Transaction Date'])
    except:
        return pd.DataFrame()

def save_to_cache(df):
    df.to_csv("cached_data.csv", index=False)
