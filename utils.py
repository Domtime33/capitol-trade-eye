import yfinance as yf
import pandas as pd

def extract_tickers_from_disclosures(df):
    tickers = df['ticker'].dropna().unique().tolist()
    return [t for t in tickers if len(t) <= 5]

def generate_recommendations(tickers, recent_df):
    top_tickers = pd.Series(tickers).value_counts().head(5).index.tolist()
    recs = []

    allocation = 10000 / len(top_tickers) if top_tickers else 0
    for ticker in top_tickers:
        try:
            stock = yf.Ticker(ticker)
            price = stock.history(period="1d")["Close"].iloc[-1]
            shares = round(allocation / price, 2)
            recs.append({"Ticker": ticker, "Price": round(price, 2), "Buy Qty": shares, "Investment": round(shares * price, 2)})
        except:
            continue

    return pd.DataFrame(recs)
