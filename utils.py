import pandas as pd
import re

def extract_tickers_from_disclosures(df):
    tickers = []
    for text in df['Asset Description'].astype(str):
        found = re.findall(r'\b[A-Z]{1,5}\b', text)
        tickers.extend(found)
    return sorted(list(set(tickers)))

def generate_recommendations(tickers, df):
    recommendations = []
    for ticker in tickers:
        subset = df[df['Asset Description'].str.contains(ticker, na=False)]
        total = len(subset)
        buy_count = len(subset[subset['Transaction'] == 'Purchase'])
        sell_count = len(subset[subset['Transaction'] == 'Sale'])

        if buy_count > sell_count:
            recommendations.append({'Ticker': ticker, 'Action': 'Buy', 'Mentions': total})
        elif sell_count > buy_count:
            recommendations.append({'Ticker': ticker, 'Action': 'Sell', 'Mentions': total})
    
    return pd.DataFrame(recommendations)
