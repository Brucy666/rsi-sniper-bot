# rsi_utils.py (RSI Signal Detection Utilities)

import pandas as pd

def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate the RSI from closing prices in a DataFrame.
    Returns a Series of RSI values.
    """
    if "close" not in df.columns or df["close"].isnull().all():
        return pd.Series(dtype=float)

    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def detect_rsi_signal(rsi_series: pd.Series) -> dict or None:
    """
    Analyze RSI Series and return a sniper signal if pattern is detected.
    Example setup: RSI V-Bounce from oversold territory.
    """
    if rsi_series is None or rsi_series.empty:
        return None

    rsi_series = rsi_series.dropna()

    if len(rsi_series) < 3:
        return None

    latest = rsi_series.iloc[-1]
    previous = rsi_series.iloc[-2]
    before_previous = rsi_series.iloc[-3]

    # Example sniper logic: oversold V bounce
    if before_previous > previous < 30 and latest > previous:
        return {
            "setup": "RSI V-Bounce",
            "rsi_now": float(latest),
            "rsi_prev": float(previous),
            "rsi_before": float(before_previous),
        }

    return None
