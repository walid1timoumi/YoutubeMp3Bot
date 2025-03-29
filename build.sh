#!/bin/bash

echo "📦 Downloading FFmpeg..."
mkdir -p ffmpeg
cd ffmpeg

curl -L -o ffmpeg.zip https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
unzip -o ffmpeg.zip

# Find the extracted folder automatically
FOLDER=$(find . -type d -name "ffmpeg*" | grep -v "__MACOSX" | head -n 1)
cd "$FOLDER"

echo "✅ FFmpeg ready in $(pwd)"

# Add FFmpeg to PATH for future use
echo "export PATH=\$PATH:$(pwd)/bin" >> $HOME/.bashrc
export PATH=$PATH:$(pwd)/bin

cd ../../
