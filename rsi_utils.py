import pandas as pd
import numpy as np

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return pd.Series(rsi, index=series.index)

def detect_rsi_signal(rsi_series):
    if rsi_series.empty or rsi_series.isna().all():
        return None

    last = rsi_series.iloc[-1]
    prev = rsi_series.iloc[-2] if len(rsi_series) > 1 else last

    if prev < 30 and last > 30:
        return "Hidden Bull Div"
    elif prev > 70 and last < 70:
        return "Hidden Bear Div"
    else:
        return None
