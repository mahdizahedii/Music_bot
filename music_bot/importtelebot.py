import os
from googleapiclient.discovery import build
import telebot
from flask import Flask, request

app = Flask(__name__)

# دریافت کلیدها از محیط متغیر
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

# بررسی اینکه کلیدها به درستی بارگذاری شده‌اند
if not TELEGRAM_BOT_TOKEN or not YOUTUBE_API_KEY:
    raise ValueError("Missing Telegram Bot Token or YouTube API Key")

# راه‌اندازی بات تلگرام
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# تابع جستجوی آهنگ در یوتیوب
def search_music(query):
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        
        # جستجو برای ویدیو
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=1
        )
        
        response = request.execute()
        
        # بررسی اینکه ویدیو پیدا شده است
        if response["items"]:
            video_id = response["items"][0]["id"]["videoId"]
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            return video_link
        else:
            return "❌ ویدیو پیدا نشد."
    except Exception as e:
        return f"خطا در جستجو: {e}"

# دستور /start
@app.route('/' + TELEGRAM_BOT_TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def index():
    return 'Music Bot is Running', 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://your-vercel-app-url/" + TELEGRAM_BOT_TOKEN)
    app.run(debug=True)
