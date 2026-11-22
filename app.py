import os
import sqlite3
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB_NAME = os.environ.get("DB_PATH", "signals.db")

TRADING_PAIRS = [
    # Live Market - Forex
    {"pair": "EUR/USD", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "GBP/USD", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "USD/JPY", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "AUD/USD", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "USD/CAD", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "USD/CHF", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "EUR/GBP", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "EUR/JPY", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "GBP/JPY", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "AUD/JPY", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "NZD/USD", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "EUR/AUD", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "EUR/CAD", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "GBP/AUD", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "GBP/CAD", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "CHF/JPY", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    {"pair": "CAD/CHF", "market": "Live market", "category": "Forex", "badge": "LIVE FOREX"},
    # Live Market - Crypto & Commodities
    {"pair": "BTC/USD", "market": "Live market", "category": "Crypto", "badge": "LIVE CRYPTO"},
    {"pair": "ETH/USD", "market": "Live market", "category": "Crypto", "badge": "LIVE CRYPTO"},
    {"pair": "XAU/USD", "market": "Live market", "category": "Commodities", "badge": "COMMODITY"},

    # OTC Market
    {"pair": "USD/ZAR (OTC)", "market": "OTC", "category": "Exotic", "badge": "OTC EXOTIC"},
    {"pair": "CAD/CHF (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "EUR/GBP (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "EUR/NZD (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "NZD/CAD (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "EUR/AUD (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "GBP/CHF (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "NZD/JPY (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "USD/MXN (OTC)", "market": "OTC", "category": "Exotic", "badge": "OTC EXOTIC"},
    {"pair": "USD/PHP (OTC)", "market": "OTC", "category": "Exotic", "badge": "OTC EXOTIC"},
    {"pair": "CHF/JPY (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "USD/COP (OTC)", "market": "OTC", "category": "Exotic", "badge": "OTC EXOTIC"},
    {"pair": "USD/PKR (OTC)", "market": "OTC", "category": "Exotic", "badge": "OTC EXOTIC"},
    {"pair": "USD/CAD (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "EUR/CAD (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "USD/DZD (OTC)", "market": "OTC", "category": "Exotic", "badge": "OTC EXOTIC"},
    {"pair": "USD/NGN (OTC)", "market": "OTC", "category": "Exotic", "badge": "OTC EXOTIC"},
    {"pair": "GBP/AUD (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "NZD/CHF (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "AUD/USD (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "AUD/JPY (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "EUR/USD (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "USD/BDT (OTC)", "market": "OTC", "category": "Exotic", "badge": "OTC EXOTIC"},
    {"pair": "USD/CHF (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "USD/IDR (OTC)", "market": "OTC", "category": "Exotic", "badge": "OTC EXOTIC"},
    {"pair": "USD/JPY (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "GBP/CAD (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "NZD/USD (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "AUD/NZD (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
    {"pair": "GBP/NZD (OTC)", "market": "OTC", "category": "Forex", "badge": "OTC FOREX"},
]

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pair TEXT NOT NULL,
            duration TEXT NOT NULL,
            direction TEXT NOT NULL,
            entry_time TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html", pairs=TRADING_PAIRS)

@app.route("/api/get_signal", methods=["POST"])
def get_signal():
    init_db()
    data = request.json or {}
    pair = data.get("pair", "EUR/USD")
    duration = data.get("duration", "5 min")

    direction = random.choice(["UP", "DOWN"])
    entry_time = datetime.now().strftime("%I:%M:%S %p")
    short_time = datetime.now().strftime("%I:%M %p")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (pair, duration, direction, entry_time) VALUES (?, ?, ?, ?)",
        (pair, duration, direction, short_time)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "pair": pair,
        "duration": duration,
        "direction": direction,
        "entry_time": entry_time,
        "short_time": short_time
    })

@app.route("/api/history", methods=["GET"])
def get_history():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT pair, duration, direction, entry_time FROM history ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall()
    conn.close()

    history_list = [
        {"pair": r[0], "duration": r[1], "direction": r[2], "entry_time": r[3]}
        for r in rows
    ]
    up_count = sum(1 for item in history_list if item["direction"] == "UP")
    down_count = sum(1 for item in history_list if item["direction"] == "DOWN")

    return jsonify({
        "total": len(history_list),
        "up": up_count,
        "down": down_count,
        "items": history_list
    })

@app.route("/api/clear_history", methods=["POST"])
def clear_history():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)