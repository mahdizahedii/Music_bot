import telebot
import time
import yt_dlp
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# دریافت توکن از فایل .env
TOKEN = os.getenv("TELEGRAM_API_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # کلید API یوتیوب خود را اینجا وارد کنید

bot = telebot.TeleBot(TOKEN)

# دیکشنری برای ذخیره زمان آخرین درخواست هر کاربر (محدودیت ضد اسپم)
user_last_request = {}

# اتصال به یوتیوب API
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# تابع جستجوی آهنگ در یوتیوب
def search_music(query):
    request = youtube.search().list(
        part="snippet",
        q=query + " song",
        type="video",
        videoDefinition="high",
        maxResults=1
    )
    response = request.execute()
    if "items" in response:
        video_url = "https://www.youtube.com/watch?v=" + response["items"][0]["id"]["videoId"]
        return video_url
    return None

# تابع دانلود آهنگ از یوتیوب
def download_audio(url, chat_id):
    file_name = f"{chat_id}.mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': file_name,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return file_name

# دستور /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎵 سلام! من یک بات موزیک هستم.\n\n✅ برای جستجوی آهنگ: `/music [نام آهنگ]`\n✅ برای دانلود آهنگ: `/download [نام آهنگ]`\n\n📢 لطفاً 10 ثانیه بین هر درخواست صبر کنید تا اسپم نشوید.")

# دستور جستجوی آهنگ
@bot.message_handler(commands=['music'])
def music(message):
    user_id = message.from_user.id
    current_time = time.time()

    # بررسی محدودیت ضد اسپم
    if user_id in user_last_request and current_time - user_last_request[user_id] < 10:
        bot.send_message(message.chat.id, "⛔ لطفاً 10 ثانیه صبر کنید و دوباره امتحان کنید.")
        return

    user_last_request[user_id] = current_time

    if len(message.text.split()) > 1:
        query = message.text.replace("/music ", "")
        result = search_music(query)
        if result:
            bot.send_message(message.chat.id, f"🎧 آهنگ پیدا شد:\n{result}")
        else:
            bot.send_message(message.chat.id, "❌ آهنگ پیدا نشد!")
    else:
        bot.send_message(message.chat.id, "❗ لطفاً نام آهنگ را بعد از /music بنویس.")

# دستور دانلود آهنگ
@bot.message_handler(commands=['download'])
def download(message):
    user_id = message.from_user.id
    current_time = time.time()

    # بررسی محدودیت ضد اسپم
    if user_id in user_last_request and current_time - user_last_request[user_id] < 10:
        bot.send_message(message.chat.id, "⛔ لطفاً 10 ثانیه صبر کنید و دوباره امتحان کنید.")
        return

    user_last_request[user_id] = current_time

    if len(message.text.split()) > 1:
        query = message.text.replace("/download ", "")
        result = search_music(query)
        if result:
            bot.send_message(message.chat.id, "⏳ در حال دانلود... لطفاً صبر کنید.")
            file_path = download_audio(result, message.chat.id)
            bot.send_audio(message.chat.id, open(file_path, 'rb'))
            os.remove(file_path)
        else:
            bot.send_message(message.chat.id, "❌ آهنگ پیدا نشد!")
    else:
        bot.send_message(message.chat.id, "❗ لطفاً نام آهنگ را بعد از /download بنویس.")

# اجرای بات
bot.polling()
