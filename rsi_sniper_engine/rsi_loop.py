# rsi_sniper_engine/rsi_loop.py (Multi-Timeframe RSI Sniper Loop)

from rsi_sniper_engine.rsi_logic import scan_rsi_sniper_map
from rsi_discord_alert import send_rsi_discord_alert
import time

def run_rsi_sniper():
    print("[LOOP] 🧠 Starting RSI Sniper Engine...")

    timeframes = [
        ("1", "1m"),
        ("3", "3m"),
        ("5", "5m"),
        ("15", "15m"),
        ("30", "30m"),
        ("60", "1h"),
        ("240", "4h")
    ]

    symbol = "BTCUSDT"

    while True:
        print("[RSI SNIPER] 🔍 Scanning for RSI sniper signal...")

        tf_map = []
        signal_summary = {"signal": None, "setup": None, "timeframe": None}

        for tf_code, tf_label in timeframes:
            try:
                signal = scan_rsi_sniper_map(symbol=symbol, interval=tf_code)
                tf_map.append((tf_label, signal["setup"] if signal else "No Signal"))

                if signal and signal.get("signal"):
                    signal_summary.update({
                        "signal": True,
                        "setup": signal["setup"],
                        "timeframe": tf_label
                    })

            except Exception as e:
                tf_map.append((tf_label, f"Error: {str(e)}"))

        if signal_summary["signal"]:
            print(f"[RSI SNIPER] ✅ Signal on {signal_summary['timeframe']} - {signal_summary['setup']}")
            signal_summary["tf_map"] = tf_map
            send_rsi_discord_alert(signal_summary)
        else:
            print("[RSI SNIPER] ❌ No signal found")

        print("[LOOP] 💤 Sleeping 60 seconds...\n")
        time.sleep(60)


if __name__ == "__main__":
    run_rsi_sniper()
