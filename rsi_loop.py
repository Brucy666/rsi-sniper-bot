from rsi_logic import scan_rsi_sniper_map
from rsi_discord_alert import send_rsi_discord_alert
import time

def run_rsi_sniper():
    print("[LOOP] 🧠 Starting RSI Sniper Engine...")
    symbol = "BTCUSDT"
    interval = "15"  # You can later loop through multiple timeframes

    while True:
        print("[RSI SNIPER] 📡 Scanning for RSI sniper signal...")
        result = scan_rsi_sniper_map(symbol=symbol, interval=interval)

        if result.get("signal"):
            print(f"[RSI SNIPER] ✅ Signal Detected: {result['setup']} @ {result['price']}")
            send_rsi_discord_alert(result)
        else:
            print("[RSI SNIPER] ❌ No signal found")

        print("[LOOP] ⏳ Sleeping 60 seconds...\n")
        time.sleep(60)

if __name__ == "__main__":
    run_rsi_sniper()
