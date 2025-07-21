import pandas as pd
import os

CACHE_FILE = "cached_data.csv"

def get_all_trade_data():
    # Replace with real scraper logic or static fallback
    return pd.read_csv("sample_disclosures.csv")  # <-- Ensure this file exists

def save_to_cache(data):
    data.to_csv(CACHE_FILE, index=False)

def get_cached_data():
    if os.path.exists(CACHE_FILE):
        return pd.read_csv(CACHE_FILE)
    return pd.DataFrame()
