import logging
import os
import re
import traceback
from urllib.parse import urlparse, parse_qs

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import yt_dlp

# ✅ FFmpeg path for Render (Linux)
FFMPEG_PATH = "ffmpeg/ffmpeg-6.1-essentials_build/bin"

# ✅ Telegram file size limit (max ~49MB)
MAX_TELEGRAM_FILE_SIZE = 49 * 1024 * 1024

# ✅ Get absolute path to cookies.txt
cookie_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')

# 🪵 Logging setup
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ✅ Clean up YouTube URLs
def clean_youtube_url(url: str) -> str:
    if "youtube.com" not in url:
        return url
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    video_id = qs.get("v", [None])[0]
    return f"https://www.youtube.com/watch?v={video_id}" if video_id else url

# 👋 Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a YouTube link and I’ll convert it to MP3!")

# 🎧 Main handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_url = update.message.text.strip()
    url = clean_youtube_url(raw_url)

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("❌ Please send a valid YouTube URL.")
        return

    await update.message.reply_text("⏳ Downloading and converting to MP3...")

    filename = None  # safe init

    try:
        print(f"[DEBUG] Cookie file path: {cookie_path}")
        print(f"[DEBUG] Cookie file exists: {os.path.exists(cookie_path)}")

        # Step 1: Extract info
        extract_opts = {
            'quiet': True,
            'ffmpeg_location': FFMPEG_PATH,
            'cookiefile': cookie_path
        }

        with yt_dlp.YoutubeDL(extract_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get("title", "audio")

        # Step 2: Clean filename
        safe_title = re.sub(r'[\\/*?:"<>|]', "", video_title)
        filename_base = safe_title
        filename = f"{filename_base}.mp3"

        # Step 3: Download config
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': filename_base,
            'ffmpeg_location': FFMPEG_PATH,
            'cookiefile': cookie_path,
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
            'verbose': True
        }

        print(f"[yt-dlp] Downloading: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if not os.path.exists(filename):
            await update.message.reply_text("❌ Failed to download or convert the video.")
            return

        size = os.path.getsize(filename)
        print(f"[DEBUG] File size: {size / (1024 * 1024):.2f} MB")

        if size > MAX_TELEGRAM_FILE_SIZE:
            await update.message.reply_text(
                f"❌ MP3 is too large to send via Telegram ({size / 1024 / 1024:.2f} MB)."
            )
        else:
            await update.message.chat.send_action(action="upload_audio")
            with open(filename, 'rb') as audio:
                await update.message.reply_audio(audio, title=video_title)

    except Exception as e:
        tb = traceback.format_exc()
        print("====== ERROR ======")
        print(tb)
        await update.message.reply_text(f"❌ Error during processing:\n{e}\n\nURL: {url}")

    finally:
        if filename and os.path.exists(filename):
            os.remove(filename)

# 🚀 Start the bot
if __name__ == '__main__':
    app = ApplicationBuilder() \
        .token(os.environ["TELEGRAM_TOKEN"]) \
        .read_timeout(120) \
        .write_timeout(120) \
        .build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
