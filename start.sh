#!/bin/bash

# Kill any previous Python processes (safely ignore if none)
pkill -f youtubemp3.py || true

# Start the bot
python youtubemp3.py
