import streamlit as st
import pandas as pd
import numpy as np
from src.data_ingestion import fetch_macro_data, fetch_market_data
from src.econometric_engine import EconometricEngine

st.title("📈 Phase 1 & 2: Macro/Micro Dashboard & Econometrics")

# Secure API key handling
FRED_KEY = st.secrets.get("FRED_API_KEY", st.text_input("Enter FRED API Key (or add to .streamlit/secrets.toml)", type="password"))
SERIES = {'CPI': 'CPIAUCSL', '10Y Treasury': 'DGS10', 'VIX': 'VIXCLS'}
TICKERS = ['SPY', 'GLD', 'TLT']

col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Start Date", pd.to_datetime('2018-01-01'))
with col2:
    end = st.date_input("End Date", pd.to_datetime('today'))

if FRED_KEY:
    macro_df = fetch_macro_data(FRED_KEY, SERIES, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
    market_df, returns_df = fetch_market_data(TICKERS, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))

    engine = EconometricEngine()

    if not returns_df.empty:
        st.subheader("Market Log Returns")
        st.line_chart(returns_df)
        
        st.subheader("Kalman Filter Signal Extraction (SPY)")
        spy_col = 'SPY' if 'SPY' in returns_df.columns else returns_df.columns[0]
        spy_returns = returns_df[spy_col].dropna()
        
        if len(spy_returns) > 0:
            try:
                # Pass BOTH the values and the dates to preserve the index!
                smoothed_state = engine.apply_kalman_filter(
                    tuple(spy_returns.values), 
                    tuple(spy_returns.index.strftime('%Y-%m-%d'))
                )
                
                df_viz = pd.DataFrame({
                    'Observed': spy_returns,
                    'Smoothed Signal': smoothed_state
                }).dropna()
                
                if len(df_viz) > 0:
                    st.line_chart(df_viz)
                else:
                    st.warning("Could not align Kalman filter results with data.")
            except Exception as e:
                st.error(f"Kalman filter error: {str(e)}")
        else:
            st.warning("No SPY return data available for the selected date range.")
    else:
        st.warning("No market data available. Check dates or API connection.")
else:
    st.warning("Please provide a valid FRED API Key to load macroeconomic data.")