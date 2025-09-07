import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime, timedelta
from core import analyze_watchlist

# --- Login Credentials ---
USERNAME = "admin"
PASSWORD = "password123"

# --- Session login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def check_login():
    if not st.session_state.logged_in:
        st.title("🔐 Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            if user == USERNAME and pwd == PASSWORD:
                st.session_state.logged_in = True
                st.success("Login successful!")
            else:
                st.error("Invalid credentials")
        st.stop()

check_login()

# --- Sidebar navigation ---
st.sidebar.title("📊 Stock Analyzer")
page = st.sidebar.radio("Navigate", ["Dashboard", "Alerts", "Custom Analysis"])

WATCHLIST = os.getenv("WATCHLIST", "AAPL,MSFT,GOOGL,AMZN,TSLA").split(",")

# --- Helper function to run analysis ---
def run_analysis():
    df = analyze_watchlist(WATCHLIST)

    alerts = []
    for _, row in df.iterrows():
        analysis = row["analysis"]
        current_price = row.get("current_price", 0)

        # Alert if near 5-week low/high
        if current_price <= analysis.get("5_weeks_low", 0) * 1.05:
            alerts.append(f"{row['ticker']} is near its 5-week low!")
        if current_price >= analysis.get("5_weeks_high", 0) * 0.95:
            alerts.append(f"{row['ticker']} is near its 5-week high!")

    # Save alerts
    with open("alerts.json", "w") as f:
        json.dump(alerts, f, indent=2)

    # Save latest analysis
    df.to_csv("latest_analysis.csv", index=False)
    return df, alerts

# --- Dashboard Page ---
if page == "Dashboard":
    st.header("📈 Latest Stock Analysis")

    if st.button("Run Analysis Now"):
        with st.spinner("Running analysis..."):
            df, alerts = run_analysis()
            st.success("✅ Analysis completed!")
    if os.path.exists("latest_analysis.csv"):
        df = pd.read_csv("latest_analysis.csv")
        st.dataframe(df)
    else:
        st.info("No analysis yet. Click 'Run Analysis Now' to start.")

# --- Alerts Page ---
elif page == "Alerts":
    st.header("🔔 Alerts")
    if os.path.exists("alerts.json"):
        with open("alerts.json", "r") as f:
            alerts = json.load(f)
        if alerts:
            for alert in alerts:
                st.success(alert)
        else:
            st.info("No alerts at this time.")
    else:
        st.warning("No alerts yet. Run analysis on Dashboard first.")

# --- Custom Analysis Page ---
elif page == "Custom Analysis":
    st.header("📝 Custom Stock Analysis")
    tickers = st.text_input("Enter stock tickers (comma-separated)", "AAPL,MSFT")
    if st.button("Analyze"):
        tickers = [t.strip() for t in tickers.split(",")]
        df = analyze_watchlist(tickers)
        st.dataframe(df)
