# rsi_utils.py

import pandas as pd

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index (RSI) using Wilder's method.
    """
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def detect_rsi_signal(rsi_series: pd.Series) -> dict or None:
    """
    Detect RSI sniper signal (RSI V-Bounce):
    - 3-bar pattern:
        rsi[-3] > rsi[-2] < 30 and rsi[-1] > rsi[-2]
    """
    if rsi_series is None or rsi_series.empty or len(rsi_series) < 3:
        return None

    rsi_series = rsi_series.dropna()

    if len(rsi_series) < 3:
        return None

    before_previous = float(rsi_series.iloc[-3])
    previous = float(rsi_series.iloc[-2])
    latest = float(rsi_series.iloc[-1])

    if before_previous > previous and previous < 30 and latest > previous:
        return {
            "setup": "RSI V-Bounce",
            "rsi_now": latest,
            "rsi_prev": previous,
            "rsi_before": before_previous
        }

    return None
