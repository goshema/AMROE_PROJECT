import streamlit as st

st.set_page_config(
    page_title="AMROE | Actuarial Market Risk & Opportunity Engine", 
    page_icon="📊", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.title("📊 Actuarial Market Risk & Opportunity Engine (AMROE)")
st.markdown("""
A rigorous, open-source statistical engine mapping market risk and opportunity using 
Probability Theory, Econometrics, and Actuarial Mathematics. 

**Core Modules:**
1. **Macro/Micro Dashboard:** Yield curves, cointegration, and Kalman filter signal extraction.
2. **Actuarial Risk Engine:** Extreme Value Theory (EVT), Tail Dependence (Copulas), VaR/ES.
3. **Opportunity & Regime Mapper:** Hidden Markov Models (HMM) and Actuarial Survival Analysis.
""")

st.sidebar.success("👈 Select a module from the navigation menu to begin.")