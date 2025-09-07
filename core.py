import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def analyze_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2y")

        if hist.empty:
            return {"ticker": ticker, "error": "No data found"}

        current_price = hist['Close'].iloc[-1]

        metrics = {}
        for weeks in [5, 13, 26, 52, 104]:  # 5 weeks → 2 years
            days = weeks * 7
            start_date = datetime.now() - timedelta(days=days)
            data = hist[hist.index >= start_date]

            if not data.empty:
                metrics[f"{weeks}_weeks_high"] = data['High'].max()
                metrics[f"{weeks}_weeks_low"] = data['Low'].min()

        return {
            "ticker": ticker,
            "current_price": current_price,
            "analysis": metrics
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}

def analyze_watchlist(watchlist):
    results = []
    for ticker in watchlist:
        results.append(analyze_stock(ticker))
    return pd.DataFrame(results)
