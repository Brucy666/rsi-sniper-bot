# rsi_logic.py

import pandas as pd

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def scan_rsi_sniper_map(df: pd.DataFrame, symbol="BTCUSDT", tf="15m") -> dict:
    close = df["close"]

    if close.empty or len(close) < 20:
        print("[RSI LOGIC] ⚠️ Not enough data for RSI.")
        return {"signal": False}

    rsi = calculate_rsi(close)

    latest_rsi = rsi.iloc[-1]
    previous_rsi = rsi.iloc[-2]

    if latest_rsi < 30 and previous_rsi > latest_rsi:
        return {
            "signal": True,
            "setup": "RSI Oversold Bounce",
            "rsi": round(latest_rsi, 2),
            "symbol": symbol,
            "timeframe": tf,
            "price": float(df["close"].iloc[-1]),
        }

    return {"signal": False}
