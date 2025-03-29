#!/bin/bash
mkdir -p ffmpeg
cd ffmpeg
curl -L -o ffmpeg.zip https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
unzip ffmpeg.zip
cd ..
