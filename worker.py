import os
import json
from datetime import datetime
from core import analyze_watchlist

def run_worker():
    watchlist = os.getenv("WATCHLIST", "AAPL,MSFT,GOOGL").split(",")
    df = analyze_watchlist(watchlist)

    alerts = []
    for _, row in df.iterrows():
        if "error" in row and row["error"]:
            continue
        analysis = row["analysis"]
        if row["current_price"] <= analysis.get("5_weeks_low", 0) * 1.05:
            alerts.append(f"{row['ticker']} is near its 5-week low!")
        if row["current_price"] >= analysis.get("5_weeks_high", 0) * 0.95:
            alerts.append(f"{row['ticker']} is near its 5-week high!")

    # Save alerts
    with open("alerts.json", "w") as f:
        json.dump(alerts, f)

    # Save latest analysis
    df.to_csv("latest_analysis.csv", index=False)

    print("Worker finished. Alerts generated:", alerts)

if __name__ == "__main__":
    run_worker()
  
