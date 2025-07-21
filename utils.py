import pandas as pd
import random

def extract_tickers_from_disclosures(df):
    tickers = df['ticker'].dropna().unique().tolist()
    return [t for t in tickers if t.isalpha()]

def generate_recommendations(tickers, df, budget=10000):
    if not tickers:
        return pd.DataFrame()

    n = len(tickers)
    allocation = budget / n

    data = {
        "Ticker": tickers,
        "Buy Amount ($)": [round(allocation, 2)] * n,
        "Rationale": [f"Mentioned in {df[df['ticker'] == t].shape[0]} recent trades" for t in tickers]
    }

    return pd.DataFrame(data)
