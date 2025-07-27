# rsi_logic.py

import pandas as pd
import numpy as np
from bybit_feed import get_bybit_ohlcv

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def detect_rsi_sniper(df):
    # Calculate RSI
    df['rsi'] = calculate_rsi(df['close'])

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    rsi_now = latest['rsi']
    rsi_prev = prev['rsi']
    close_now = latest['close']
    close_prev = prev['close']

    # Placeholder signal logic (you can make this smarter)
    if rsi_now < 30 and close_now > close_prev:
        return "Bullish RSI Reversal"
    elif rsi_now > 70 and close_now < close_prev:
        return "Bearish RSI Rejection"
    else:
        return None

def scan_rsi_sniper_map(symbol="BTCUSDT", interval="15"):
    df = get_bybit_ohlcv(symbol=symbol, interval=interval)

    if df is None or df.empty:
        return {
            "symbol": symbol,
            "interval": interval,
            "signal": None,
            "setup": "No data",
            "rsi_value": None
        }

    signal = detect_rsi_sniper(df)

    return {
        "symbol": symbol,
        "interval": interval,
        "signal": bool(signal),
        "setup": signal if signal else "No Signal",
        "rsi_value": df['rsi'].iloc[-1] if "rsi" in df else None
    }
