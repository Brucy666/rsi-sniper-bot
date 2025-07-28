# rsi_utils.py (RSI Calculation + Signal Detection)

import pandas as pd

def calculate_rsi(close_prices: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate RSI from close prices using Wilder's method.
    """
    if close_prices is None or close_prices.empty:
        return pd.Series(dtype=float)

    delta = close_prices.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))

    return rsi


def detect_rsi_signal(rsi_series: pd.Series) -> dict or None:
    """
    Detects RSI V-Bounce pattern:
    - rsi[-3] > rsi[-2] < 30
    - rsi[-1] > rsi[-2]
    """
    if rsi_series is None or rsi_series.empty:
        return None

    rsi_series = rsi_series.dropna()

    if len(rsi_series) < 3:
        return None

    try:
        rsi_3 = float(rsi_series.iloc[-3])
        rsi_2 = float(rsi_series.iloc[-2])
        rsi_1 = float(rsi_series.iloc[-1])
    except Exception:
        return None

    if rsi_3 > rsi_2 < 30 and rsi_1 > rsi_2:
        return {
            "setup": "RSI V-Bounce",
            "rsi_now": rsi_1,
            "rsi_prev": rsi_2,
            "rsi_before": rsi_3
        }

    return None
