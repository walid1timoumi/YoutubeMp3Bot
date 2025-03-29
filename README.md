# YouTube to MP3 Telegram Bot

A Telegram bot that converts YouTube videos to MP3 audio files and sends them directly to users.

![Bot Demo](https://i.imgur.com/JK7ZENP.png) *(example screenshot placeholder)*

## Features

- 🎵 Convert YouTube videos to high-quality MP3 (192kbps)
- 🔗 Supports both `youtube.com` and `youtu.be` URLs
- 🧹 Automatically cleans URLs (removes playlist parameters, timestamps, etc.)
- 📦 Handles files up to Telegram's 50MB limit
- ⚡ Fast conversion using `yt-dlp` and `FFmpeg`
- 💾 Automatic cleanup of temporary files

## Requirements

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- `ffmpeg` (included in the project)
- Render.com account (for deployment)

## Installation

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/youtube-mp3-bot.git
   cd youtube-mp3-bot
Install dependencies:

bash
Copy
pip install -r requirements.txt
Set up environment variables:

bash
Copy
echo "TELEGRAM_TOKEN=your_bot_token_here" > .env
Run the bot:

bash
Copy
python bot.py
Render Deployment
Create a new Web Service on Render

Set environment variables:

TELEGRAM_TOKEN: Your Telegram bot token

Use the following build commands:

bash
Copy
# Build Command
unzip ffmpeg.zip -d ffmpeg
pip install -r requirements.txt
Set the start command:

bash
Copy
python bot.py
Usage
Start a chat with your bot on Telegram

Send any YouTube URL (e.g., https://youtube.com/watch?v=dQw4w9WgXcQ)

The bot will:

Download the video

Convert to MP3

Send the audio file back to you

Commands:

/start - Show welcome message

Configuration
Environment variables:

TELEGRAM_TOKEN (required) - Your Telegram bot token

FFMPEG_PATH - Path to FFmpeg binaries (default included)

Technical Details
Uses yt-dlp for YouTube downloading (superior to youtube-dl)

FFmpeg for audio conversion (pre-configured for Render)

Automatic filename sanitization

Error handling and logging

File size checking (won't attempt to send >50MB files)

Limitations
Telegram has a 50MB file size limit

Some videos may be blocked by YouTube

Processing time depends on video length and server resources

Contributing
Pull requests are welcome! Please ensure:

Your code follows PEP8 style

You've tested your changes

You've updated documentation as needed

License
MIT License - See LICENSE file

Support
For issues, please open a GitHub issue
