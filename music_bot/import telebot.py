import os
from googleapiclient.discovery import build
import telebot

# دریافت کلیدها از محیط متغیر
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

# راه‌اندازی بات تلگرام
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# تابع جستجوی آهنگ در یوتیوب
def search_music(query):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=1
    )
    
    response = request.execute()
    
    if response["items"]:
        video_id = response["items"][0]["id"]["videoId"]
        video_link = f"https://www.youtube.com/watch?v={video_id}"
        return video_link
    else:
        return None
