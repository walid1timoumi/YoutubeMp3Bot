#!/bin/bash

echo "🔁 Stopping any existing Python Telegram bot instances..."

# Kill any existing Python scripts (non-fatal if not found)
pkill -f youtubemp3.py || echo "✅ No previous bot process found."

echo "🚀 Starting Telegram bot..."
python3 youtubemp3.py
