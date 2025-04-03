import os
import logging
import shutil
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot_debug.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Constants
MAX_FILE_SIZE = 49 * 1024 * 1024  # 49MB Telegram limit
FFMPEG_PATH = shutil.which("ffmpeg") or "ffmpeg"
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Now loaded from .env file

# YouTube configuration
COOKIE_PATH = os.getenv("COOKIE_PATH", "/app/cookies.txt")
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15',
    'com.google.android.youtube/17.36.4 (Linux; U; Android 11)'
]

# Validate critical configurations
if not BOT_TOKEN:
    logging.error("Missing BOT_TOKEN in environment variables!")
    exit(1)