import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR, VECM
from statsmodels.tsa.statespace.structural import UnobservedComponents
from arch import arch_model

class EconometricEngine:
    @st.cache_resource(show_spinner="Fitting VAR Model...")
    def fit_var_model(_self, data: pd.DataFrame, maxlags: int = 5):
        model = VAR(data.dropna())
        return model.fit(maxlags=maxlags, ic='aic')

    @st.cache_resource(show_spinner="Fitting VECM Model...")
    def fit_vecm_model(_self, data: pd.DataFrame, k_ar_diff: int = 1, coint_rank: int = 1):
        model = VECM(data.dropna(), k_ar_diff=k_ar_diff, coint_rank=coint_rank)
        return model.fit()

    @st.cache_resource(show_spinner="Fitting GARCH Model...")
    def fit_garch(_self, returns: pd.Series, p: int = 1, q: int = 1, model_type: str = 'GARCH'):
        clean_returns = returns.dropna() * 100
        model = arch_model(clean_returns, vol=model_type, p=p, q=q, dist='t')
        return model.fit(disp='off')

    @st.cache_data(show_spinner="Applying Kalman Filter...")
    def apply_kalman_filter(_self, observed_values: tuple, index_dates: tuple) -> pd.Series:
        # Reconstruct the series with the correct datetime index
        series = pd.Series(observed_values, index=pd.to_datetime(index_dates)).dropna()
        
        if len(series) < 30:
            return series.rolling(window=min(10, len(series)), min_periods=1).mean()
        
        try:
            model = UnobservedComponents(series, level='local level')
            results = model.fit(disp=False)
            smoothed_level = results.smoothed_state[0]
            smoothed_signal = pd.Series(smoothed_level, index=series.index)
            return smoothed_signal
        except Exception as e:
            print(f"Kalman filter failed: {e}")
            return series.rolling(window=20, min_periods=1).mean()