# send_approval.py
import os
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BASE_URL = os.environ.get("BASE_URL")
bot = Bot(token=BOT_TOKEN)

def send_approval(chat_id, user_id, username):
    url = f"{BASE_URL}/start/{user_id}/{username}"
    keyboard = [[InlineKeyboardButton("Enter the wheel of fortune 🍀", url=url)]]
    text = "🎉 Your request has been approved!\nNow you can enter the wheel of fortune! 🍀\nClick below to start."
    bot.send_message(chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == "__main__":
    # for testing, send to admin (ensure env vars set)
    target_chat_id = int(os.environ.get("ADMIN_CHAT_ID"))
    sample_user_id = int(os.environ.get("ADMIN_CHAT_ID"))
    sample_username = "yourusername"
    send_approval(target_chat_id, sample_user_id, sample_username)
    print("Sent approval test message.")