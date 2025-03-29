import logging
import os
import re
import traceback
import shutil
from urllib.parse import urlparse, parse_qs

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import yt_dlp

# ✅ Automatically find ffmpeg location
FFMPEG_PATH = os.path.dirname(shutil.which("ffmpeg"))

# ✅ Telegram file size limit
MAX_TELEGRAM_FILE_SIZE = 49 * 1024 * 1024

# ✅ Absolute path to cookies.txt
cookie_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')

# 🪵 Logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ✅ Clean YouTube URLs
def clean_youtube_url(url: str) -> str:
    if "youtube.com" not in url:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        video_id = qs.get("v", [None])[0]
        return f"https://www.youtube.com/watch?v={video_id}" if video_id else url
    return url

# 👋 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a YouTube link and I’ll convert it to MP3!")

# 🎧 Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_url = update.message.text.strip()
    url = clean_youtube_url(raw_url)

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("❌ Please send a valid YouTube URL.")
        return

    await update.message.reply_text("⏳ Downloading and converting to MP3...")
    filename = None

    try:
        print(f"[DEBUG] FFmpeg path: {FFMPEG_PATH}")
        print(f"[DEBUG] Cookie file: {cookie_path} Exists: {os.path.exists(cookie_path)}")

        with open(cookie_path, "r") as f:
            print("🔐 Cookie file preview:")
            for _ in range(10):
                print(f.readline().strip())

        # Step 1: Extract info
        extract_opts = {
            'quiet': True,
            'ffmpeg_location': FFMPEG_PATH,
            'cookiefile': cookie_path
        }

        with yt_dlp.YoutubeDL(extract_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get("title", "audio")

        # Step 2: Sanitize
