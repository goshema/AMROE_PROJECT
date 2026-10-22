import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import genpareto, rankdata, t
from lifelines import CoxPHFitter
from hmmlearn.hmm import GaussianHMM
import warnings
warnings.filterwarnings('ignore')

class ActuarialRiskModels:
    @st.cache_data(show_spinner="Calculating EVT & Tail Risk...")
    def evt_gpd_var_es(_self, returns_tuple: tuple, confidence_level: float = 0.99, threshold_quantile: float = 0.95):
        returns_series = pd.Series(returns_tuple)
        losses = -returns_series[returns_series < 0]
        u = np.quantile(losses, threshold_quantile)
        excesses = losses[losses > u] - u
        
        n = len(losses)
        N_u = len(excesses)
        
        if N_u < 30:
            var = np.quantile(losses, confidence_level)
            es = losses[losses > var].mean() if not losses[losses > var].empty else var
            return var, es, np.nan, np.nan, "Historical Simulation (Insufficient Tail Data)"
        
        xi, _, sigma = genpareto.fit(excesses, floc=0)
        var = u + (sigma / xi) * (((1 - confidence_level) / (N_u / n))**(-xi) - 1)
        es = var + (sigma + xi * (var - u)) / (1 - xi)
        return var, es, xi, sigma, "EVT-GPD"

    @st.cache_resource(show_spinner="Fitting Copula...")
    def fit_copula(_self, data: pd.DataFrame, copula_type: str = 't'):
        # Calculate pseudo-observations (Empirical CDF)
        pobs = rankdata(data.values, axis=0) / (len(data) + 1)
        pobs_df = pd.DataFrame(pobs, columns=data.columns, index=data.index)
        
        # For visualization purposes, we just return the data
        # Actual copula fitting requires more complex parameter estimation
        return pobs_df

    @st.cache_resource(show_spinner="Fitting Cox Proportional Hazards...")
    def cox_proportional_hazards(_self, survival_data: pd.DataFrame, duration_col: str, event_col: str, covariates: list):
        cph = CoxPHFitter()
        cols_to_keep = [duration_col, event_col] + covariates
        subset_data = survival_data[cols_to_keep].dropna().copy()
        cph.fit(subset_data, duration_col=duration_col, event_col=event_col)
        return cph

    @st.cache_resource(show_spinner="Fitting HMM Regimes...")
    def fit_hmm_regimes(_self, returns_tuple: tuple, n_states: int = 3):
        returns_series = pd.Series(returns_tuple).dropna()
        values = returns_series.values.reshape(-1, 1)
        
        model = GaussianHMM(n_components=n_states, covariance_type="full", n_iter=1000, random_state=42)
        model.fit(values)
        
        means = model.means_.flatten()
        sorted_indices = np.argsort(means)
        model.state_mapping_ = {int(old_idx): int(new_idx) for new_idx, old_idx in enumerate(sorted_indices)}
        
        return model, returns_series.index