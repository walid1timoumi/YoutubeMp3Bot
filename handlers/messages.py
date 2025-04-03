import logging
import os
import asyncio
from io import BytesIO
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
from telegram.error import TimedOut
from utils.youtube import is_valid_youtube_url, get_audio_url
from utils.file_handling import download_mp3, cleanup_file

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = update.message.text.strip()
        logging.info(f"Processing URL: {url}")

        if not is_valid_youtube_url(url):
            await update.message.reply_text(
                "❌ Invalid YouTube URL\n"
                "Please send a direct video link like:\n"
                "• https://www.youtube.com/watch?v=...\n"
                "• https://youtu.be/...",
                disable_web_page_preview=True
            )
            return

        processing_msg = await update.message.reply_text(
            "🔍 Checking video availability...",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{update.effective_user.id}")]
            ])
        )

        try:
            audio_url, title = await get_audio_url(url)
            await processing_msg.edit_text(f"🎧 Found: {title[:60]}...\n⬇️ Downloading audio...", parse_mode=None)

            try:
                filename = await asyncio.wait_for(
                    download_mp3(audio_url, title, update, context),
                    timeout=90
                )

                if filename and os.path.exists(filename):
                    with open(filename, 'rb') as f:
                        audio_data = BytesIO(f.read())
                        audio_data.name = os.path.basename(filename)

                    try:
                        await context.bot.send_audio(
                            chat_id=update.effective_chat.id,
                            audio=InputFile(audio_data),
                            title=title
                        )
                        await processing_msg.edit_text(f"✅ Sent: {title[:60]}...")

                    except TimedOut:
                        logging.warning("Telegram timed out, but likely sent successfully.")
                        # Do not send any error to user
                        await processing_msg.edit_text(f"✅ Sent (maybe delayed): {title[:60]}...")

                    await cleanup_file(filename)

                else:
                    await processing_msg.edit_text("⚠️ Download failed. Try another video.")

            except asyncio.TimeoutError:
                logging.warning("Download timed out")
                await processing_msg.edit_text(
    "⚠️ Couldn't process this video\n\n"
    "Reason: Timed out\n\n"
    "Try another video or check:\n"
    "1. Video is public\n"
    "2. Not age-restricted\n"
    "3. Available in your region",
    parse_mode=None
)


        except Exception as e:
            logging.exception("Processing failed")
            await processing_msg.edit_text(
    f"⚠️ Couldn't process this video\n\n"
    f"Reason: {str(e)}\n\n"
    "Try another video or check:\n"
    "1. Video is public\n"
    "2. Not age-restricted\n"
    "3. Available in your region",
    parse_mode=None
)


    except Exception as e:
        logging.exception("Handler crashed")
        await update.message.reply_text(
            "⚠️ An unexpected error occurred\n"
            "Please try again later"
        )
