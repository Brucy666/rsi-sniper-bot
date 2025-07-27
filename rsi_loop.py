# rsi_loop.py - Master RSI Sniper Loop

from rsi_logic import scan_rsi_sniper_map
from rsi_discord_alert import send_rsi_discord_alert
from bybit_feed import get_bybit_ohlcv
import time


def run_rsi_sniper():
    print("[LOOP] 🧠 Starting RSI Sniper Bot...")

    while True:
        print("[RSI SNIPER] 🔍 Scanning for RSI signals...")

        result = scan_rsi_sniper_map(symbol="BTCUSDT")

        if result.get("signal"):
            print(f"[RSI SNIPER] ✅ Signal on {result['timeframe']} - {result['setup']}")
            send_rsi_discord_alert(result)
        else:
            print("[RSI SNIPER] ❌ No signal detected")

        print("[LOOP] 💤 Sleeping 60 seconds\n")
        time.sleep(60)


if __name__ == "__main__":
    run_rsi_sniper()
