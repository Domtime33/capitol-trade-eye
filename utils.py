def extract_tickers_from_disclosures(df):
    tickers = []
    for _, row in df.iterrows():
        tickers += [t.strip().upper() for t in row.get("Ticker", "").split(",") if t.strip()]
    return list(set(tickers))

def generate_recommendations(tickers, df):
    import pandas as pd
    top_picks = []
    for ticker in tickers:
        count = df["Ticker"].str.contains(ticker, case=False).sum()
        if count >= 2:  # Customize threshold
            top_picks.append({"Ticker": ticker, "Mentions": count, "Suggested Buy ($10K)": round(10000 / len(tickers), 2)})

    return pd.DataFrame(top_picks)
