# rsi_loop.py (Standalone RSI Sniper Bot Main Loop)

import time
from rsi_logic import scan_rsi_sniper_map
from rsi_discord_alert import send_rsi_discord_alert


def run_rsi_sniper():
    print("[LOOP] 🎯 Starting RSI Sniper Engine...")

    while True:
        print("[RSI SNIPER] 🔍 Scanning for RSI sniper signal...")

        try:
            result = scan_rsi_sniper_map(symbol="BTCUSDT", interval="15m")

            if result.get("signal"):
                print(f"[RSI SNIPER] ✅ Signal found: {result['signal']} on {result['timeframe']}")
                send_rsi_discord_alert(result)
            else:
                print("[RSI SNIPER] ❌ No signal found")

        except Exception as e:
            print(f"[ERROR] Failed to fetch data or process signal: {e}")

        print("[LOOP] 💤 Sleeping 60 seconds...\n")
        time.sleep(60)


if __name__ == "__main__":
    run_rsi_sniper()
