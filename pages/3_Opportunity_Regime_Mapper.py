import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.data_ingestion import fetch_market_data
from src.actuarial_models import ActuarialRiskModels

st.title("🧭 Phase 3 & 4: Opportunity & Regime Mapper")

market_df, returns_df = fetch_market_data(['SPY'], '2010-01-01', pd.to_datetime('today').strftime('%Y-%m-%d'))
actuarial = ActuarialRiskModels()

if not returns_df.empty:
    spy_col = 'SPY' if 'SPY' in returns_df.columns else returns_df.columns[0]
    spy_returns = returns_df[spy_col].dropna()
    
    st.subheader("Hidden Markov Model (HMM) Market Regimes")
    n_states = st.slider("Number of Latent States", 2, 4, 3)
    
    model, dates_index = actuarial.fit_hmm_regimes(tuple(spy_returns), n_states)
    raw_states = model.predict(spy_returns.values.reshape(-1, 1))
    
    # Apply consistent state mapping (0=Bear, 1=Neutral, 2=Bull)
    mapped_states = [model.state_mapping_[int(s)] for s in raw_states]
    
    df_hmm = pd.DataFrame({'Return': spy_returns.values, 'State': mapped_states}, index=dates_index)
    
    fig = px.scatter(
        df_hmm, x=df_hmm.index, y='Return', color='State', 
        title="Market Regimes Identified by HMM (Sorted by Mean Return)", 
        color_continuous_scale=px.colors.sequential.Viridis,
        hover_data=['Return']
    )
    fig.update_layout(xaxis_title="Date", yaxis_title="Daily Log Return")
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Actuarial Survival Analysis: Market Regime Longevity")
    st.write("Cox Proportional Hazards model estimating the survival probability of the current market regime given macro covariates.")
    
    # Mock survival data for UI demonstration
    np.random.seed(42)
    n = 1000
    mock_data = pd.DataFrame({
        'duration': np.random.exponential(50, n),
        'event': np.random.binomial(1, 0.8, n),
        'volatility': np.random.normal(0.2, 0.05, n),
        'yield_curve': np.random.normal(1.5, 0.5, n)
    })
    
    cph = actuarial.cox_proportional_hazards(mock_data, 'duration', 'event', ['volatility', 'yield_curve'])
    
    # Predict survival function safely
    surv_df = cph.predict_survival_function(pd.DataFrame({'volatility': [0.2], 'yield_curve': [1.5]}))
    
    fig_surv = px.line(
        x=surv_df.index, 
        y=surv_df.iloc[:, 0], 
        title="Survival Function of Market Regime",
        labels={'x': 'Days', 'y': 'Survival Probability'}
    )
    st.plotly_chart(fig_surv, use_container_width=True)