import pandas as pd
import os
from datetime import datetime
import json

CACHE_FILE = "cached_trades.csv"

def get_all_trade_data():
    # Simulated or scraped trade data (replace with real scraper later)
    data = pd.read_csv("sample_trades.csv")  # Replace with actual scraping logic
    data['Transaction Date'] = pd.to_datetime(data['Transaction Date'])
    return data

def save_to_cache(data):
    data.to_csv(CACHE_FILE, index=False)

def get_cached_data():
    if os.path.exists(CACHE_FILE):
        data = pd.read_csv(CACHE_FILE)
        data['Transaction Date'] = pd.to_datetime(data['Transaction Date'])
        return data
    return pd.DataFrame()
