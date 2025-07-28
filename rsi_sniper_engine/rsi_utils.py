# rsi_utils.py (Fixed version for RSI Sniper Bot)

import pandas as pd

def calculate_rsi(df_or_series, period: int = 14) -> pd.Series:
    """
    Accepts a DataFrame or Series and calculates RSI.
    """

    # Normalize input to Series of close prices
    if isinstance(df_or_series, pd.DataFrame):
        if "close" not in df_or_series.columns:
            return pd.Series(dtype=float)
        close = df_or_series["close"]
    elif isinstance(df_or_series, pd.Series):
        close = df_or_series
    else:
        return pd.Series(dtype=float)

    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def detect_rsi_signal(rsi_series: pd.Series) -> dict or None:
    """
    Detect RSI sniper signal (e.g. V-Bounce from oversold).
    """
    if rsi_series is None or rsi_series.empty:
        return None

    rsi_series = rsi_series.dropna()
    if len(rsi_series) < 3:
        return None

    latest = rsi_series.iloc[-1]
    previous = rsi_series.iloc[-2]
    before_previous = rsi_series.iloc[-3]

    # V-bounce pattern
    if before_previous > previous < 30 and latest > previous:
        return {
            "setup": "RSI V-Bounce",
            "rsi_now": float(latest),
            "rsi_prev": float(previous),
            "rsi_before": float(before_previous),
        }

    return None
