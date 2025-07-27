# rsi_logic.py

import pandas as pd
from bybit_feed import get_bybit_ohlcv


def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def scan_rsi_sniper_map(symbol="BTCUSDT", interval="15"):
    try:
        df = get_bybit_ohlcv(symbol=symbol, interval=interval)
        if df is None or df.empty:
            return {"signal": None, "reason": "No data"}

        df['rsi'] = calculate_rsi(df['close'], period=14)

        latest_rsi = df['rsi'].iloc[-1]
        latest_price = df['close'].iloc[-1]

        signal = None
        if latest_rsi < 30:
            signal = "RSI Oversold"
        elif latest_rsi > 70:
            signal = "RSI Overbought"

        return {
            "symbol": symbol,
            "interval": interval,
            "signal": bool(signal),
            "setup": signal if signal else "No Signal",
            "price": float(latest_price),
            "rsi": round(float(latest_rsi), 2)
        }

    except Exception as e:
        return {"signal": None, "reason": f"Exception: {str(e)}"}
