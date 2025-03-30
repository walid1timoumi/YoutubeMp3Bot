import os
import re
import requests
import logging
import shutil
import traceback
import subprocess
from urllib.parse import urlparse, parse_qs

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# ✅ Logging setup
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# ✅ File size limit (Telegram max)
MAX_TELEGRAM_FILE_SIZE = 49 * 1024 * 1024  # 49 MB

# ✅ Use system ffmpeg path
FFMPEG_PATH = shutil.which("ffmpeg")

# ✅ Clean YouTube URL and get video ID
def extract_video_id(url: str) -> str | None:
    parsed = urlparse(url)
    if "youtu.be" in url:
        return parsed.path[1:]
    qs = parse_qs(parsed.query)
    return qs.get("v", [None])[0]

# ✅ Get stream info from Piped (updated API)
def get_audio_url(video_id: str):
    piped_apis = [
        "https://pipedapi.adminforge.de",
        "https://pipedapi.tokhmi.xyz",
        "https://pipedapi.in.projectsegfau.lt",
        "https://pipedapi.kavin.rocks",  # might fail
    ]

    for api in piped_apis:
        try:
            logging.info(f"[🔁] Trying Piped API: {api}")
            r = requests.get(f"{api}/streams/{video_id}", timeout=10)
            r.raise_for_status()
            data = r.json()

            audio_streams = data.get("audioStreams", [])
            if not audio_streams:
                continue

            best_audio = audio_streams[0]
            return best_audio["url"], data.get("title", "audio")
        except Exception as e:
            logging.warning(f"[⚠️] Failed with {api}: {e}")
            continue

    return None, None

# ✅ Download audio via ffmpeg
def download_mp3(audio_url, title):
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    filename = f"{safe_title}.mp3"

    result = subprocess.run([
        FFMPEG_PATH,
        "-y",
        "-i", audio_url,
        "-vn",
        "-acodec", "libmp3lame",
        "-b:a", "192k",
        "-movflags", "+faststart",
        filename
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return filename if os.path.exists(filename) else None

# 👋 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a YouTube link and I’ll convert it to MP3 (proxy mode, no login required)!")

# 🎧 Main handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    video_id = extract_video_id(url)

    if not video_id:
        await update.message.reply_text("❌ Invalid YouTube link.")
        return

    await update.message.reply_text("🔄 Converting to MP3...")

    filename = None
    try:
        audio_url, title = get_audio_url(video_id)
        if not audio_url:
            await update.message.reply_text("❌ No audio stream found.")
            return

        filename = download_mp3(audio_url, title)
        if not filename:
            await update.message.reply_text("❌ Failed to convert audio.")
            return

        size = os.path.getsize(filename)
        if size > MAX_TELEGRAM_FILE_SIZE:
            await update.message.reply_text("❌ MP3 is too large to send via Telegram.")
            return

        await update.message.chat.send_action(action="upload_audio")
        with open(filename, 'rb') as f:
            await update.message.reply_audio(f, title=title)

    except Exception as e:
        print(traceback.format_exc())
        await update.message.reply_text(f"❌ Error: {e}")

    finally:
        if filename and os.path.exists(filename):
            os.remove(filename)

# 🚀 Bot runner
if __name__ == "__main__":
    app = ApplicationBuilder() \
        .token(os.environ["TELEGRAM_TOKEN"]) \
        .read_timeout(120) \
        .write_timeout(120) \
        .build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
