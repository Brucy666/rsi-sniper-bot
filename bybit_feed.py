import requests
import pandas as pd

def get_ohlcv_data(symbol: str, interval: str) -> pd.DataFrame:
    url = f"https://api.bybit.com/v5/market/kline?category=linear&symbol={symbol}&interval={interval}&limit=200"
    try:
        res = requests.get(url).json()
        rows = res.get("result", {}).get("list", [])
        if not rows:
            return pd.DataFrame()

        df = pd.DataFrame(rows, columns=[
            "timestamp", "open", "high", "low", "close", "volume", "turnover"
        ])
        df = df.astype(float)
        df["rsi"] = df["close"].rolling(14).apply(compute_rsi, raw=False)
        return df
    except Exception as e:
        print(f"[ERROR] Failed to fetch data: {e}")
        return pd.DataFrame()

def compute_rsi(series):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0.0).rolling(14).mean()
    rs = gain / (loss + 1e-10)
    return 100 - (100 / (1 + rs))
