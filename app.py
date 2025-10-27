# app.py
import os
import sqlite3
from datetime import datetime
from flask import Flask, request, render_template, jsonify
from telegram import Bot, ParseMode

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", "0"))
BASE_URL = os.environ.get("BASE_URL", "https://example.com")  # update on Render env

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment variables")

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__, static_folder='static', template_folder='templates')

DB = 'wins.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS wins (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 username TEXT,
                 prize TEXT,
                 timestamp TEXT
                 )""")
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return "Wheel Bot is running."

@app.route("/start/<int:tg_user_id>/<username>")
def start_wheel(tg_user_id, username):
    # Renders the wheel page and injects user info
    return render_template("wheel.html", user_id=tg_user_id, username=username, base_url=BASE_URL)

@app.route("/result", methods=["POST"])
def result():
    data = request.json or {}
    user_id = data.get("user_id")
    username = data.get("username", "")
    prize = data.get("prize", "")
    timestamp = datetime.utcnow().isoformat()

    # Save to DB
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO wins (user_id, username, prize, timestamp) VALUES (?,?,?,?)",
                  (user_id, username, prize, timestamp))
        conn.commit()
        conn.close()
    except Exception as e:
        print("DB error:", e)

    # Notify user
    try:
        bot.send_message(int(user_id),
                         text=f"🎉 Congratulations! You won: *{prize}* 🎁\nCheck the wheel page for details.",
                         parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        print("Error sending message to user:", e)

    # Notify admin
    try:
        admin_text = f"🎡 Wheel result:\nUser: {username} (`{user_id}`)\nPrize: *{prize}*\nTime: {timestamp}"
        bot.send_message(ADMIN_CHAT_ID, text=admin_text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        print("Error sending to admin:", e)

    return jsonify({"status":"ok"})