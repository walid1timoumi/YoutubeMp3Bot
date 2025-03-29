# 🎧 YouTube to MP3 Telegram Bot

A Telegram bot that converts YouTube videos to MP3 audio files and sends them directly to users — all within a few seconds.

![Bot Demo](https://imgur.com/a/MCUxDIm) <!-- Example screenshot placeholder -->

---

## 🚀 Features

- 🎵 Convert YouTube videos to high-quality MP3 (192kbps)
- 🔗 Supports both `youtube.com` and `youtu.be` links
- 🧹 Cleans URLs by removing unnecessary parameters
- 📦 Handles files up to Telegram’s 50MB limit
- ⚡ Fast conversion using `yt-dlp` and `FFmpeg`
- 🧼 Auto-cleans temp files after each download

---

## 📦 Requirements

- Python 3.8+
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- FFmpeg (included in project or system-installed)
- [Render.com](https://render.com) account for deployment (optional)

---

## 🧑‍💻 Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/youtube-mp3-bot.git
cd youtube-mp3-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

```bash
echo "TELEGRAM_TOKEN=your_bot_token_here" > .env
```

### 4. Run the Bot

```bash
python bot.py
```

---

## 🌐 Deployment on Render

1. Create a new **Web Service** on [Render](https://render.com/).
2. Set the environment variable:

   - `TELEGRAM_TOKEN`: Your Telegram bot token

3. Use this **build command**:

```bash
unzip ffmpeg.zip -d ffmpeg
pip install -r requirements.txt
```

4. Set the **start command**:

```bash
python bot.py
```

---

## 💡 Usage

1. Start a conversation with your bot on Telegram.
2. Send any valid YouTube link (e.g. `https://youtube.com/watch?v=dQw4w9WgXcQ`).
3. The bot will:
   - ⬇️ Download the video
   - 🔄 Convert to MP3
   - 📤 Send the MP3 audio back to you

### Available Commands

- `/start` – Show welcome message

---

## ⚙️ Configuration

| Variable        | Description                       |
|----------------|-----------------------------------|
| `TELEGRAM_TOKEN` | ✅ Required. Your bot token from BotFather |
| `FFMPEG_PATH`    | Optional. Path to FFmpeg binaries (default included) |

---

## 🔍 Technical Details

- Uses `yt-dlp` for YouTube downloads (better than `youtube-dl`)
- Uses `FFmpeg` for audio extraction
- Auto-sanitizes filenames to prevent OS issues
- Prevents sending files over 50MB
- Handles logging and exceptions gracefully

---

## ⚠️ Limitations

- Telegram bots cannot send files larger than **50MB**
- YouTube may restrict some videos due to region or copyright
- Download time depends on video length and server performance

---

## 🤝 Contributing

Pull requests are welcome! Before submitting:

- Follow PEP8 style conventions
- Test your code
- Update documentation if needed

---

## 📄 License

This project is licensed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 🛟 Support

For issues or feature requests, please [open a GitHub issue](https://github.com/yourusername/youtube-mp3-bot/issues).

---
