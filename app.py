import streamlit as st
import os
import json
import pandas as pd
from core import analyze_watchlist

USERNAME = "admin"
PASSWORD = "password123"

def check_login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

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

def main():
    check_login()
    st.sidebar.title("📊 Stock Analyzer")
    page = st.sidebar.radio("Navigate", ["Dashboard", "Alerts", "Custom Analysis"])

    if page == "Dashboard":
        st.header("📈 Latest Stock Analysis")
        if os.path.exists("latest_analysis.csv"):
            df = pd.read_csv("latest_analysis.csv")
            st.dataframe(df)
        else:
            st.warning("No analysis available yet. Wait for worker to run.")

    elif page == "Alerts":
        st.header("🔔 Alerts")
        if os.path.exists("alerts.json"):
            with open("alerts.json", "r") as f:
                alerts = json.load(f)
            if alerts:
                for alert in alerts:
                    st.success(alert)
            else:
                st.info("No alerts right now.")
        else:
            st.warning("No alerts available yet.")

    elif page == "Custom Analysis":
        st.header("📝 Custom Stock Analysis")
        tickers = st.text_input("Enter stock tickers (comma-separated)", "AAPL,MSFT")
        if st.button("Analyze"):
            tickers = [t.strip() for t in tickers.split(",")]
            df = analyze_watchlist(tickers)
            st.dataframe(df)

if __name__ == "__main__":
    main()
