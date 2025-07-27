import os
import requests
from datetime import datetime

DISCORD_WEBHOOK = os.getenv("DISCORD_RSI_WEBHOOK")

def send_rsi_discord_alert(data):
    if not DISCORD_WEBHOOK:
        print("[❌] No webhook set")
        return

    embed = {
        "title": "📈 RSI Signal Detected",
        "color": 0x00ff99,
        "fields": [
            {"name": "Symbol", "value": data["symbol"], "inline": True},
            {"name": "Setup", "value": data["setup"], "inline": True},
            {"name": "RSI", "value": f"{data['rsi']:.2f}", "inline": True},
            {"name": "Timeframe", "value": data["timeframe"], "inline": True},
            {"name": "Price", "value": f"{data['price']}", "inline": True},
            {"name": "Timestamp", "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"), "inline": False},
        ],
        "footer": {"text": "RSI Sniper Engine"}
    }

    try:
        res = requests.post(DISCORD_WEBHOOK, json={"embeds": [embed]}, headers={"Content-Type": "application/json"})
        if res.status_code in [200, 204]:
            print("[✅] RSI alert sent to Discord.")
        else:
            print(f"[❌] Discord send failed: {res.status_code}, {res.text}")
    except Exception as e:
        print(f"[❌] Discord exception: {e}")
