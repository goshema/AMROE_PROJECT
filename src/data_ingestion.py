import os
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from fredapi import Fred
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

@st.cache_data(ttl=3600, show_spinner="Fetching macroeconomic data...")
def fetch_macro_data(fred_api_key: str, series_dict: dict, start_date: str, end_date: str, db_path: str = "data/amroe_state.db") -> pd.DataFrame:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    macro_df = pd.DataFrame()
    
    try:
        fred = Fred(api_key=fred_api_key)
        for name, series_id in series_dict.items():
            data = fred.get_series(series_id, observation_start=start_date, observation_end=end_date)
            macro_df[name] = data
        
        macro_df = macro_df.resample('D').ffill()
        macro_df.to_sql('macro_data', conn, if_exists='replace', index=True, index_label='date')
        logging.info("Macro data fetched and saved to SQLite.")
        
    except Exception as e:
        logging.error(f"FRED API Error: {e}. Falling back to SQLite.")
        try:
            macro_df = pd.read_sql('SELECT * FROM macro_data', conn, parse_dates=['date'], index_col='date')
        except Exception as db_e:
            logging.error(f"SQLite fallback failed: {db_e}")
            
    finally:
        conn.close()
    return macro_df

@st.cache_data(ttl=3600, show_spinner="Fetching market data...")
def fetch_market_data(tickers: list, start_date: str, end_date: str, db_path: str = "data/amroe_state.db") -> tuple:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    market_df = pd.DataFrame()
    returns_df = pd.DataFrame()
    
    try:
        data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True, progress=False)
        
        if isinstance(data.columns, pd.MultiIndex):
            market_df = data['Close']
        else:
            market_df = data[['Close']].rename(columns={'Close': tickers[0]})
            
        market_df = market_df.resample('D').ffill()
        returns_df = np.log(market_df / market_df.shift(1)).dropna()
        
        market_df.to_sql('market_data', conn, if_exists='replace', index=True, index_label='date')
        returns_df.to_sql('market_returns', conn, if_exists='replace', index=True, index_label='date')
        logging.info("Market data fetched and saved to SQLite.")
        
    except Exception as e:
        logging.error(f"yfinance API Error: {e}. Falling back to SQLite.")
        try:
            market_df = pd.read_sql('SELECT * FROM market_data', conn, parse_dates=['date'], index_col='date')
            returns_df = pd.read_sql('SELECT * FROM market_returns', conn, parse_dates=['date'], index_col='date')
        except Exception as db_e:
            logging.error(f"SQLite fallback failed: {db_e}")
            
    finally:
        conn.close()
    return market_df, returns_df