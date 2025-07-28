# ✅ rsi_loop.py (Multi-Timeframe RSI Sniper Loop)

from rsi_sniper_engine.rsi_logic import scan_rsi_sniper_map
from rsi_discord_alert import send_rsi_discord_alert
import time


def run_rsi_sniper():
    print("[LOOP] 🧠 Starting RSI Sniper Engine...")

    while True:
        print("[RSI SNIPER] 🔎 Scanning for RSI sniper signal...")

        tf_map, signal_summary = scan_rsi_sniper_map(symbol="BTCUSDT")

        if isinstance(signal_summary, dict) and signal_summary.get("signal"):
            print(f"[RSI SNIPER] ✅ Signal on {signal_summary['timeframe']} - {signal_summary['setup']}")
            signal_summary["tf_map"] = tf_map
            send_rsi_discord_alert(signal_summary)
        else:
            print("[RSI SNIPER] ❌ No signal found")

        print("[LOOP] 💤 Sleeping 60 seconds...\n")
        time.sleep(60)


if __name__ == "__main__":
    run_rsi_sniper()
