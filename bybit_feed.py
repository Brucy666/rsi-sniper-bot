# bybit_feed.py

import requests
import pandas as pd
import time

def get_bybit_ohlcv(symbol="BTCUSDT", interval="15", limit=200):
    try:
        resolution = interval
        endpoint = f"https://api.bybit.com/v5/market/kline"
        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": resolution,
            "limit": limit
        }

        response = requests.get(endpoint, params=params)
        data = response.json()

        if "result" not in data or "list" not in data["result"]:
            print("[BYBIT_FEED] ❌ Invalid response format")
            return None

        ohlcv_raw = data["result"]["list"]
        ohlcv_raw.reverse()  # newest last

        df = pd.DataFrame(ohlcv_raw, columns=[
            "timestamp", "open", "high", "low", "close", "volume", "_turnover"
        ])

        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(float), unit="ms")
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
        return df

    except Exception as e:
        print(f"[BYBIT_FEED] ⚠️ Error fetching OHLCV: {e}")
        return None
