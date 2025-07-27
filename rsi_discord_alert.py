# rsi_discord_alert.py

import requests
import os
from datetime import datetime

DISCORD_WEBHOOK = os.getenv("DISCORD_RSI_WEBHOOK")

def send_rsi_discord_alert(data: dict):
    if not DISCORD_WEBHOOK:
        print("[❌] No Discord webhook provided.")
        return

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    color = 0x00ff90 if "Oversold" in data["setup"] else 0xff5555

    embed = {
        "title": "🎯 RSI Signal Detected",
        "color": color,
        "fields": [
            {"name": "Token", "value": f"`{data['symbol']}`", "inline": True},
            {"name": "Timeframe", "value": f"`{data['interval']}`", "inline": True},
            {"name": "Price", "value": f"`{data['price']}`", "inline": True},
            {"name": "RSI", "value": f"`{data['rsi']}`", "inline": True},
            {"name": "Setup", "value": f"`{data['setup']}`", "inline": True},
            {"name": "Timestamp", "value": f"`{timestamp}`", "inline": False}
        ],
        "footer": {"text": "RSI Sniper AI Engine"}
    }

    payload = {"username": "RSI Sniper Bot", "embeds": [embed]}

    try:
        res = requests.post(DISCORD_WEBHOOK, json=payload)
        if res.status_code in [200, 204]:
            print("[✓] RSI alert sent to Discord.")
        else:
            print(f"[❌] Discord response error: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[❌] Failed to send Discord alert: {str(e)}")
