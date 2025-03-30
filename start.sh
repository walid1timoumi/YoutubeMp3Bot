#!/bin/bash

echo "🔍 FFmpeg version:"
which ffmpeg
ffmpeg -version

echo "✅ Starting your Telegram bot..."
python3 youtubemp3.py
