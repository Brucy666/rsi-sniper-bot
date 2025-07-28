# rsi_sniper_engine/rsi_logic.py (AI RSI Multi-TF Sniper)

import pandas as pd
from bybit_feed import get_bybit_ohlcv
from rsi_sniper_engine.rsi_utils import calculate_rsi, detect_rsi_signal

def scan_rsi_sniper_map(symbol="BTCUSDT"):
    timeframes = [
        ("1", "1m"),
        ("3", "3m"),
        ("5", "5m"),
        ("15", "15m"),
        ("30", "30m"),
        ("60", "1h"),
        ("240", "4h")
    ]

    tf_results = {}
    signal_found = None

    for tf_code, tf_label in timeframes:
        df = get_bybit_ohlcv(symbol=symbol, interval=tf_code)

        if df is None or df.empty or len(df) < 20:
            tf_results[tf_label] = "No Data"
            continue

        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df.dropna(subset=["close"], inplace=True)
        df["rsi"] = calculate_rsi(df["close"], period=14)

        signal = detect_rsi_signal(df)
        tf_results[tf_label] = signal["type"] if signal else "No Signal"

        if not signal_found and signal:
            signal_found = {
                "symbol": symbol,
                "timeframe": tf_label,
                "setup": signal["type"],
                "strength": signal.get("strength", 0),
                "rsi": df["rsi"].iloc[-1],
                "tf_map": tf_results
            }

    return signal_found if signal_found else {"signal": None, "tf_map": tf_results}
