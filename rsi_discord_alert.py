# rsi_discord_alert.py (Discord Alert Sender for RSI Sniper Bot)

import os
import requests
from datetime import datetime

DISCORD_WEBHOOK = os.getenv("DISCORD_RSI_WEBHOOK")

def format_discord_alert(data: dict) -> dict:
    symbol = data.get("symbol", "BTCUSDT")
    tf = data.get("timeframe", "N/A")
    signal = data.get("signal", "N/A")
    rsi_value = data.get("rsi", 0)
    entry_price = data.get("price", 0)
    confidence = data.get("confidence", 0)
    bias = data.get("bias", "N/A")
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    color = 0x00ff00 if "Bull" in signal else 0xff0000 if "Bear" in signal else 0xcccccc
    brain = "🧠" if confidence >= 7 else "⚠️" if confidence >= 4 else "❓"
    bias_emoji = "📈" if bias == "above" else "📉"

    return {
        "username": "RSI Sniper Bot",
        "embeds": [
            {
                "title": f"🎯 RSI Signal Detected",
                "color": color,
                "fields": [
                    {"name": "Symbol", "value": f"`{symbol}`", "inline": True},
                    {"name": "Timeframe", "value": f"`{tf}`", "inline": True},
                    {"name": "Signal", "value": f"`{signal}`", "inline": True},
                    {"name": "RSI", "value": f"`{rsi_value}`", "inline": True},
                    {"name": "Entry Price", "value": f"`{entry_price}`", "inline": True},
                    {"name": "Bias", "value": f"{bias_emoji} `{bias}`", "inline": True},
                    {"name": "Confidence", "value": f"{brain} `{confidence}/10`", "inline": True},
                    {"name": "Timestamp", "value": f"`{timestamp}`", "inline": False},
                ],
                "footer": {"text": "RSI Multi-Timeframe AI Engine"}
            }
        ]
    }

def send_rsi_discord_alert(data: dict):
    if not DISCORD_WEBHOOK:
        print("[RSI ALERT] ❌ Missing DISCORD_RSI_WEBHOOK environment variable.")
        return

    payload = format_discord_alert(data)
    headers = {"Content-Type": "application/json"}

    try:
        res = requests.post(DISCORD_WEBHOOK, json=payload, headers=headers)
        if res.status_code in [200, 204]:
            print("[RSI ALERT] ✅ Alert sent to Discord.")
        else:
            print(f"[RSI ALERT] ❌ Failed to send alert: {res.status_code} {res.text}")
    except Exception as e:
        print(f"[RSI ALERT] ❌ Exception during send: {e}")
