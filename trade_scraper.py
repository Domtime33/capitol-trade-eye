import requests
import pandas as pd
import json
from datetime import datetime

CACHE_FILE = "cache.json"

def get_all_trade_data():
    url = "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json"
    response = requests.get(url)
    trades = response.json()

    df = pd.DataFrame(trades)
    df['Transaction Date'] = pd.to_datetime(df['transaction_date'])
    df = df[df['ticker'].notna()]
    df = df[df['transaction'].isin(["Purchase", "Sale"])]
    return df

def save_to_cache(df):
    df.to_json(CACHE_FILE, orient='records')

def get_cached_data():
    try:
        with open(CACHE_FILE, 'r') as f:
            cached = json.load(f)
        return pd.DataFrame(cached)
    except:
        return pd.DataFrame()
