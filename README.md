# 🎧 Youtube MP3 Telegram Bot

A powerful Telegram bot that downloads audio from any YouTube video and sends it back to the user as an `.mp3` file — with Docker support, clean logging, and error handling.

## 🚀 Features

- ✅ Convert **YouTube videos to MP3** via link
- ✅ Works with **public Telegram channels or chats**
- ✅ Automatic file cleanup after sending
- ✅ Timeout handling and retry logic
- ✅ Detailed error messages for common issues (age restriction, private videos, etc.)
- ✅ Built-in support for **Docker**
- ✅ Clean project structure with `handlers`, `utils`, and `.env`-based config
- ✅ Logs saved in `bot_debug.log` for debugging

## 📦 Tech Stack

- Python 3.11
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- ffmpeg (for audio processing)
- Docker (containerization)

## 🛠 Project Structure

```
YoutubeMp3Bot/
├── handlers/              # Telegram command + message handlers
├── utils/                 # YouTube download logic and file tools
├── tmp/                   # Temporary mp3 files (auto-deleted)
├── main.py                # Bot entry point
├── config.py              # Loads secrets from .env
├── .env                   # Your BOT_TOKEN and FFMPEG_PATH (ignored)
├── .gitignore             # Prevent secrets and cache from being pushed
├── Dockerfile             # Container setup
└── docker-compose.yml     # Run with one command
```

## 📦 Installation (Local)

```bash
git clone https://github.com/yourusername/YoutubeMp3Bot.git
cd YoutubeMp3Bot

# Create virtual env (optional)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo BOT_TOKEN=your_bot_token_here > .env
echo FFMPEG_PATH=ffmpeg >> .env

# Run the bot
python main.py
```

## 🐳 Docker Setup

> Easiest way to run in production

### 🔧 1. Build and run
```bash
docker compose up --build
```

### 🔁 2. Or run manually
```bash
docker build -t youtube-mp3-bot .
docker run --env-file .env -v ${PWD}/tmp:/app/tmp youtube-mp3-bot
```

## 📄 Example Usage

In Telegram:
1. Start the bot
2. Send a YouTube link like: `https://www.youtube.com/watch?v=xxxx`
3. The bot will reply with an `.mp3` file

## ⚠️ Notes

- Only supports **public videos** (not age-restricted, blocked, etc.)
- Uses `yt-dlp` + `ffmpeg` inside the container
- Secrets (tokens) are never pushed thanks to `.gitignore`

---

### 📬 Credits
Built with ❤️ by Walid — Dockerized and bulletproof.