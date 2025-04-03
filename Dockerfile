# Base Python image
FROM python:3.11-slim

# Disable cache + buffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Install system dependencies (including ffmpeg and ffprobe)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all bot files
COPY . .

# Expose volume for audio
VOLUME /app/tmp

# Run the bot
CMD ["python", "main.py"]
