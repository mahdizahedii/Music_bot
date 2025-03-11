import os
from googleapiclient.discovery import build
import telebot
from flask import Flask, request

# دریافت توکن و API Key از متغیرهای محیطی
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

# بررسی مقداردهی درست
if not TELEGRAM_BOT_TOKEN or not YOUTUBE_API_KEY:
    raise ValueError("Missing Telegram Bot Token or YouTube API Key")

# ایجاد نمونه بات تلگرام
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ایجاد یک اپلیکیشن Flask برای مدیریت Webhook
app = Flask(__name__)

# تنظیم Webhook (این مقدار را تغییر نده)
WEBHOOK_URL = f"https://music-bot-two.vercel.app/{TELEGRAM_BOT_TOKEN}"

# تنظیم مسیر Webhook برای دریافت پیام‌ها
@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# دستور /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎵 سلام! من یک بات موزیک هستم.\n\n✅ برای جستجوی آهنگ: `/music [نام آهنگ]`\n\n")

# دستور /music برای جستجوی آهنگ
@bot.message_handler(commands=['music'])
def music(message):
    if len(message.text.split()) > 1:
        query = message.text.replace("/music ", "")
        bot.send_message(message.chat.id, f"🔎 جستجو برای: {query}")
    else:
        bot.send_message(message.chat.id, "❗ لطفاً نام آهنگ را بعد از /music بنویس.")

# راه‌اندازی Webhook هنگام شروع برنامه
@app.route("/")
def index():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    return "Webhook Set!", 200

# اجرای برنامه Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
