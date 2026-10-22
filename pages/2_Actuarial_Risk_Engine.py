import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.data_ingestion import fetch_market_data
from src.actuarial_models import ActuarialRiskModels
from src.backtesting import Backtester

st.title("🛡️ Phase 3: Actuarial Risk Engine")

TICKERS = ['SPY', 'GLD', 'TLT']
market_df, returns_df = fetch_market_data(TICKERS, '2018-01-01', pd.to_datetime('today').strftime('%Y-%m-%d'))
actuarial = ActuarialRiskModels()
backtester = Backtester()

if not returns_df.empty:
    spy_col = 'SPY' if 'SPY' in returns_df.columns else returns_df.columns[0]
    spy_returns = returns_df[spy_col].dropna()
    
    st.subheader("Extreme Value Theory (EVT) Tail Risk")
    var, es, xi, sigma, method = actuarial.evt_gpd_var_es(tuple(spy_returns))
    
    st.info(f"**Model Used:** {method} | **Shape (ξ):** {xi:.4f} | **Scale (σ):** {sigma:.4f}")
    col1, col2 = st.columns(2)
    col1.metric("99% Value at Risk (VaR)", f"{var:.2%}")
    col2.metric("Expected Shortfall (ES / CVaR)", f"{es:.2%}")
    
    # Backtesting logging
    exceptions = np.sum(spy_returns < -var)
    p_val_kupiec = backtester.kupiec_pof_test(exceptions, len(spy_returns), 0.99)
    backtester.log_backtest("EVT_VaR_99", p_val_kupiec)
    st.caption(f"Kupiec POF Test p-value: {p_val_kupiec:.4f} (Pass if >= 0.05)")
    
    st.subheader("Tail Dependence: Copula Analysis (SPY vs GLD)")
    gld_col = 'GLD' if 'GLD' in returns_df.columns else returns_df.columns[1]
    
    if gld_col in returns_df.columns:
        copula_data = returns_df[[spy_col, gld_col]].dropna()
        actuarial.fit_copula(copula_data, 't') # Fits and caches
        
        fig = go.Figure(data=go.Scattergl(
            x=copula_data[spy_col], 
            y=copula_data[gld_col], 
            mode='markers',
            marker=dict(color=np.linspace(0, 1, len(copula_data)), colorscale='Viridis', size=4, opacity=0.6)
        ))
        fig.update_layout(title="Joint Return Distribution (Tail Dependence Visualization)", xaxis_title=spy_col, yaxis_title=gld_col)
        st.plotly_chart(fig, use_container_width=True)