#!/bin/bash

echo "🔍 Verifying FFmpeg..."
which ffmpeg
ffmpeg -version

echo "✅ Starting your Telegram bot..."

# Optional: kill any stuck Python processes (advanced safety, use with care)
# pkill -f youtubemp3.py || true

python youtubemp3.py
