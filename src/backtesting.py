import numpy as np
import pandas as pd
import scipy.stats as stats
import sqlite3
import os

class Backtester:
    def kupiec_pof_test(self, exceptions: int, total_obs: int, var_confidence: float):
        p = 1 - var_confidence
        x = exceptions if exceptions > 0 else 1
        N = total_obs
        lr_pof = -2 * np.log(((1 - p)**(N - x)) * (p**x)) + 2 * np.log(((1 - x/N)**(N - x)) * ((x/N)**x))
        return 1 - stats.chi2.cdf(lr_pof, df=1)

    def christoffersen_test(self, exceptions_series: pd.Series):
        ind = exceptions_series.values.astype(int)
        n = len(ind)
        n00 = np.sum((ind[1:] == 0) & (ind[:-1] == 0))
        n01 = np.sum((ind[1:] == 1) & (ind[:-1] == 0))
        n10 = np.sum((ind[1:] == 0) & (ind[:-1] == 1))
        n11 = np.sum((ind[1:] == 1) & (ind[:-1] == 1))
        
        if (n00 + n01) == 0 or (n10 + n11) == 0:
            return 1.0 
            
        pi01 = n01 / (n00 + n01)
        pi11 = n11 / (n10 + n11)
        pi = (n01 + n11) / (n00 + n01 + n10 + n11)
        
        L0 = ((1 - pi)**(n00 + n10)) * (pi**(n01 + n11))
        L1 = ((1 - pi01)**n00) * (pi01**n01) * ((1 - pi11)**n10) * (pi11**n11)
        
        if L0 == 0 or L1 == 0:
            return 0.0
            
        lr_ind = -2 * np.log(L0 / L1)
        return 1 - stats.chi2.cdf(lr_ind, df=1)

    def log_backtest(self, model_name: str, p_value: float, db_path: str = "data/amroe_state.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS backtest_logs
                          (timestamp TEXT, model_name TEXT, p_value REAL, status TEXT)''')
        
        status = "PASS" if p_value >= 0.05 else "FAIL_RECALIBRATE"
        cursor.execute("INSERT INTO backtest_logs VALUES (datetime('now'), ?, ?, ?)", (model_name, p_value, status))
        conn.commit()
        conn.close()
        
        if status == "FAIL_RECALIBRATE":
            print(f"WARNING: {model_name} failed backtest. Triggering parameter recalibration loop...")