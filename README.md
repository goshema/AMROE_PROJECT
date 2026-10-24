# AMROE - Actuarial Market Risk & Opportunity Engine

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---
**Build using Qwen-3.7Pluse AI model for validation and debugging** 

## 📊 Overview

**AMROE** (Actuarial Market Risk & Opportunity Engine) is a rigorous, open-source quantitative analysis platform that bridges the gap between actuarial mathematics, econometrics, and modern portfolio theory. Built with Python and Streamlit, this application provides institutional-grade risk analytics and market regime detection in an accessible web interface.

Unlike traditional trading dashboards that rely on simple technical indicators, AMROE employs advanced statistical methods including Extreme Value Theory (EVT), Copula-based tail dependence analysis, Hidden Markov Models (HMM), and Kalman filter signal extraction to provide a comprehensive view of market risk and opportunity.

---

## 🎯 Why This Project Was Created

Modern financial markets are increasingly complex, with traditional risk models often failing to capture tail risks and regime shifts. The 2008 financial crisis and subsequent market events demonstrated that standard Gaussian assumptions and simple VaR models are insufficient for capturing extreme market behavior.

---

##  How It Works: The Logic Behind AMROE

### Core Architecture

AMROE follows a modular, three-phase analytical pipeline:

```
Data Ingestion → Econometric Processing → Actuarial Risk Assessment → Visualization
```

### Phase 1: Macro/Micro Dashboard & Signal Extraction

**Kalman Filter Signal Extraction**
- **What it does**: Separates the "signal" (true market trend) from "noise" (random daily fluctuations)
- **How it works**: Uses a state-space model where the observed market returns are treated as noisy measurements of an unobserved "true" trend. The Kalman filter recursively estimates this hidden state, providing a smoothed signal that reveals the underlying market direction
- **Why it matters**: Helps identify whether a market move is a genuine trend or just random noise, reducing false signals

**Macroeconomic Integration**
- Pulls real-time data from the Federal Reserve Economic Data (FRED) API
- Tracks key indicators: CPI (inflation), 10-Year Treasury yields, VIX (volatility)
- Caches data locally in SQLite for fast retrieval and offline analysis

### Phase 2: Actuarial Risk Engine

**Extreme Value Theory (EVT) - Generalized Pareto Distribution (GPD)**
- **What it does**: Models the probability of extreme market crashes (tail events)
- **How it works**: Instead of assuming returns follow a normal distribution (which underestimates extreme events), EVT focuses specifically on the tail of the distribution. It fits a Generalized Pareto Distribution to losses that exceed a high threshold
- **Key metrics**:
  - **Value at Risk (VaR)**: The maximum expected loss at a given confidence level (e.g., 99%)
  - **Expected Shortfall (ES/CVaR)**: The average loss given that we've exceeded the VaR threshold
- **Why it matters**: Provides more accurate risk estimates for extreme events than traditional parametric methods

**Copula Analysis - Tail Dependence**
- **What it does**: Measures how assets move together during market crashes
- **How it works**: Uses Student-t Copulas to model the joint distribution of asset returns, specifically capturing "tail dependence" - the tendency for assets to crash together
- **Why it matters**: Reveals hidden correlations that only appear during stress periods, crucial for portfolio diversification

**Backtesting - Kupiec POF Test**
- **What it does**: Validates whether our risk models are accurate
- **How it works**: Compares the number of actual exceptions (days where losses exceeded VaR) to the expected number. Uses statistical hypothesis testing to determine if the model is reliable
- **Why it matters**: Ensures the risk metrics can be trusted for decision-making

### Phase 3: Opportunity & Regime Mapper

**Hidden Markov Models (HMM)**
- **What it does**: Identifies distinct market "regimes" (e.g., Bull, Bear, High Volatility)
- **How it works**: Assumes the market switches between hidden states, each with different return distributions. The HMM learns these states from historical data and classifies each day into a regime
- **Why it matters**: Different strategies work in different regimes. Trend-following works in bull markets, while mean-reversion works in range-bound markets

**Actuarial Survival Analysis - Cox Proportional Hazards**
- **What it does**: Estimates how long the current market regime is likely to last
- **How it works**: Borrowed from medical research (where it predicts patient survival), this model estimates the "survival probability" of the current market state given various covariates (volatility, yield curve shape, etc.)
- **Why it matters**: Helps answer "Is this bull market about to end?" with statistical rigor

---

##  Real-World Applications

### 1. Portfolio Risk Management
- **Use Case**: A portfolio manager uses AMROE to calculate the 99% Expected Shortfall of their holdings
- **Benefit**: More accurate capital allocation and stress testing than traditional VaR models
- **Example**: Before a major position, check the EVT metrics to understand worst-case scenarios

### 2. Market Regime Detection
- **Use Case**: A quantitative trader uses the HMM module to identify whether the market is in a bull, bear, or transition state
- **Benefit**: Adjust trading strategies based on the identified regime (e.g., reduce leverage in bear markets)
- **Example**: When HMM detects a shift to "high volatility" regime, automatically tighten stop-losses

### 3. Tail Risk Hedging
- **Use Case**: An institutional investor uses Copula analysis to understand how their portfolio assets correlate during crashes
- **Benefit**: Identify "diversification illusions" where assets appear uncorrelated normally but crash together
- **Example**: Discover that stocks and corporate bonds have high tail dependence, prompting additional hedging

### 4. Academic Research
- **Use Case**: A finance PhD student uses AMROE to test hypotheses about market efficiency and risk pricing
- **Benefit**: Open-source, reproducible research with institutional-grade methods
- **Example**: Study whether Kalman filter signals can predict future returns

### 5. Actuarial Applications
- **Use Case**: An insurance company uses the survival analysis module to model the duration of market conditions affecting their investment portfolio
- **Benefit**: Better asset-liability matching and capital planning
- **Example**: Estimate the probability that a low-interest-rate environment persists for 5+ years

---

## 🚀 Getting Started: Installation & Setup

### Prerequisites

Before you begin, ensure you have:
- **Python 3.8 or higher** installed ([Download Python](https://www.python.org/downloads/))
- **Git** installed ([Download Git](https://git-scm.com/))
- A **FRED API Key** (free) from [FRED API](https://fred.stlouisfed.org/docs/api/api_key.html)

### Step 1: Clone the Repository

Open your terminal (Command Prompt, PowerShell, or Terminal) and run:

```bash
git clone https://github.com/goshema/AMROE_PROJECT.git
cd AMROE_PROJECT
```

### Step 2: Create a Virtual Environment

It's highly recommended to use a virtual environment to avoid dependency conflicts:

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

### Step 3: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (web framework)
- Pandas & NumPy (data manipulation)
- yfinance (market data)
- fredapi (economic data)
- statsmodels (econometrics)
- arch (GARCH models)
- hmmlearn (Hidden Markov Models)
- lifelines (survival analysis)
- plotly (interactive visualizations)
- Riskfolio-Lib (portfolio optimization)

*Note: Installation may take 3-5 minutes depending on your internet speed.*

### Step 4: Configure Your API Key

Create a secrets file to store your FRED API key securely:

1. Create a `.streamlit` folder in the project root (if it doesn't exist):
   ```bash
   mkdir .streamlit
   ```

2. Create a `secrets.toml` file inside `.streamlit`:
   ```bash
   notepad .streamlit/secrets.toml
   ```

3. Add your FRED API key (replace with your actual key):
   ```toml
   FRED_API_KEY = "your_32_character_api_key_here"
   ```

4. Save and close the file.

*Alternative: You can also enter your API key directly in the web interface when the app runs.*

### Step 5: Run the Application

Start the Streamlit server:

```bash
streamlit run app.py
```

Your default web browser will automatically open to `http://localhost:8501` with the AMROE dashboard.

---

##  Project Structure

```
amroe_project/
│
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── secrets.toml               # API keys and secrets (gitignored)
│
├── src/                            # Core logic modules
│   ├── __init__.py                # Package initializer
│   ├── data_ingestion.py          # Data fetching and caching
│   ├── econometric_engine.py      # Kalman filters, VAR, GARCH
│   ├── actuarial_models.py        # EVT, Copulas, HMM, Survival Analysis
│   └── backtesting.py             # Model validation
│
── pages/                          # Streamlit multi-page app
│   ├── 1_Macro_Micro_Dashboard.py # Phase 1: Macro data & Kalman filters
│   ├── 2_Actuarial_Risk_Engine.py # Phase 2: EVT, Copulas, VaR/ES
│   └── 3_Opportunity_Regime_Mapper.py  # Phase 3: HMM & Survival Analysis
│
└── data/                           # Local SQLite database (auto-created)
    └── amroe_state.db
```

---

## 🎮 How to Use AMROE

### Daily Workflow

1. **Morning Analysis (Before Market Open)**
   - Navigate to **Macro/Micro Dashboard**
   - Check the Kalman Filter signal: Is the smoothed trend crossing below observed prices? This indicates weakening momentum
   - Review macroeconomic indicators (VIX, yield curve)

2. **Risk Assessment**
   - Go to **Actuarial Risk Engine**
   - Check your 99% Expected Shortfall: This is your worst-case average loss
   - Verify the Kupiec p-value: If < 0.05, your risk model needs recalibration
   - Examine the Copula scatter plot: Are your assets showing high tail dependence?

3. **Regime Detection**
   - Open **Opportunity & Regime Mapper**
   - Identify the current market regime (Bull/Bear/Transition)
   - Check the survival curve: How long is this regime likely to persist?
   - Adjust your strategy accordingly

### Customization

**Change Tracked Assets:**
Edit `pages/1_Macro_Micro_Dashboard.py` and `pages/2_Actuarial_Risk_Engine.py`:
```python
TICKERS = ['SPY', 'GLD', 'TLT', 'AAPL', 'BTC-USD']  # Add your assets
```

**Change Macroeconomic Indicators:**
Edit `pages/1_Macro_Micro_Dashboard.py`:
```python
SERIES = {
    'CPI': 'CPIAUCSL',
    '10Y Treasury': 'DGS10',
    'VIX': 'VIXCLS',
    'M2 Money Supply': 'M2SL',  # Add more indicators
    'Yield Curve': 'T10Y2Y'
}
```

---

## 🔧 Troubleshooting

### Common Issues

**1. "Module not found" errors**
- Ensure your virtual environment is activated: `.\venv\Scripts\Activate.ps1` (Windows) or `source venv/bin/activate` (Mac/Linux)
- Reinstall dependencies: `pip install -r requirements.txt`

**2. Kalman filter shows flat line**
- This is a known issue with certain data ranges. Try adjusting the date range in the dashboard
- The app will automatically fall back to a 20-day rolling mean if the Kalman filter fails

**3. FRED API errors**
- Verify your API key is correct in `.streamlit/secrets.toml`
- Check that you have no trailing spaces in the key
- Ensure your internet connection is stable

**4. Port already in use**
- If you get an error about port 8501 being in use, run: `streamlit run app.py --server.port 8502`

---

## 📊 Technical Details

### Data Sources
- **Market Data**: Yahoo Finance via `yfinance` library (free, no API key required)
- **Macroeconomic Data**: Federal Reserve Economic Data (FRED) API (free API key required)
- **Data Caching**: SQLite database for fast retrieval and offline analysis

### Statistical Methods
- **Kalman Filter**: Local level state-space model for signal extraction
- **EVT-GPD**: Peaks-over-threshold method for tail risk modeling
- **Student-t Copula**: Captures tail dependence between assets
- **Gaussian HMM**: 3-state regime detection with full covariance matrices
- **Cox Proportional Hazards**: Semi-parametric survival model

### Performance
- First load may take 10-20 seconds as data is fetched and models are fitted
- Subsequent loads are faster due to Streamlit's caching mechanism
- Data is cached for 1 hour (3600 seconds) by default

---

##  Contributing

Contributions are welcome! This is an open-source project aimed at democratizing quantitative finance. If you have suggestions for:
- New risk models
- Additional data sources
- UI/UX improvements
- Bug fixes

Please open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Federal Reserve Bank of St. Louis** for providing free access to FRED economic data
- **Yahoo Finance** for market data via yfinance
- **Streamlit** for the amazing web framework
- The quantitative finance and actuarial science communities for the mathematical foundations

---

## 📧 Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub or reach out directly.

---

**Built with ❤️ for the quantitative finance community**

*Disclaimer: This tool is for educational and research purposes only. It does not constitute financial advice. Always consult with a qualified financial advisor before making investment decisions.*
```
