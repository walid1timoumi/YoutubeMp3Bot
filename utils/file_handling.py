import subprocess
import os
import re
import asyncio
import logging
import yt_dlp
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import FFMPEG_PATH

TMP_DIR = "tmp"

def sanitize_filename(title: str) -> str:
    """Sanitize filename with strict validation"""
    return re.sub(r'[\\/*?:"<>|\x00-\x1f]', "", title)[:100].strip()

def ensure_tmp_dir():
    """Ensure the tmp/ folder exists"""
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

async def download_mp3(audio_url: str, title: str, 
                      update: Optional[Update] = None, 
                      context: Optional[ContextTypes.DEFAULT_TYPE] = None) -> Optional[str]:
    """Enhanced downloader with progress tracking"""
    ensure_tmp_dir()
    safe_title = sanitize_filename(title)
    filename = os.path.join(TMP_DIR, f"{safe_title}.mp3")
    progress_msg = None

    try:
        if update and context:
            progress_msg = await send_progress_message(update, context, "⬇️ Starting download...")

        # Method 1: Direct streaming conversion
        for protocol in ['https', 'http']:
            try:
                modified_url = audio_url.replace('https://', f'{protocol}://')
                if await try_direct_conversion(modified_url, filename, progress_msg):
                    return filename
            except Exception as e:
                logging.warning(f"Protocol {protocol} failed: {str(e)}")
                continue

        # Method 2: Download-then-convert fallback
        return await fallback_conversion(audio_url, filename, safe_title, progress_msg)

    except Exception as e:
        if progress_msg:
            await handle_download_error(e, progress_msg)
        return None
    finally:
        if progress_msg:
            try:
                await progress_msg.delete()
            except Exception as e:
                logging.warning(f"Failed to delete progress message: {str(e)}")

async def send_progress_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """Send initial progress message with cancel button"""
    return await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{update.effective_user.id}")]
        ])
    )

async def try_direct_conversion(url: str, output_path: str, progress_msg) -> bool:
    """Attempt direct streaming conversion"""
    if progress_msg:
        await progress_msg.edit_text("🔧 Converting stream...")

    ffmpeg_cmd = [
        FFMPEG_PATH, "-y",
        "-protocol_whitelist", "file,http,https,tcp,tls",
        "-reconnect", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "5",
        "-i", url,
        "-vn", "-c:a", "libmp3lame", "-b:a", "192k", "-threads", "2",
        output_path
    ]

    try:
        process = await asyncio.create_subprocess_exec(
            *ffmpeg_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        await process.wait()
        return process.returncode == 0 and os.path.exists(output_path)
    except Exception as e:
        logging.error(f"Direct conversion failed: {str(e)}")
        if os.path.exists(output_path):
            os.remove(output_path)
        return False

async def fallback_conversion(url: str, output_path: str, temp_prefix: str, progress_msg) -> Optional[str]:
    """Fallback download-then-convert method"""
    if progress_msg:
        await progress_msg.edit_text("🔄 Trying fallback method...")

    temp_file = os.path.join(TMP_DIR, f"{temp_prefix}.temp")
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': temp_file,
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await asyncio.to_thread(ydl.download, [url])

        for ext in ['.mp3', '.webm', '.m4a']:
            temp_output = f"{temp_file}{ext}"
            if os.path.exists(temp_output):
                os.rename(temp_output, output_path)
                return output_path

        return None
    except Exception as e:
        logging.error(f"Fallback conversion failed: {str(e)}")
        return None
    finally:
        for file_to_remove in [
            temp_file,
            f"{temp_file}.mp3",
            f"{temp_file}.webm",
            f"{temp_file}.m4a"
        ]:
            if os.path.exists(file_to_remove):
                try:
                    os.remove(file_to_remove)
                except Exception as e:
                    logging.warning(f"Could not remove temp file {file_to_remove}: {str(e)}")

async def handle_download_error(error: Exception, progress_msg) -> None:
    """Handle download errors and update user"""
    error_msg = str(error)[:200]
    logging.error(f"Download error: {error_msg}")
    
    if progress_msg:
        try:
            await progress_msg.edit_text(f"⚠️ Error: {error_msg}")
        except Exception as e:
            logging.error(f"Failed to update error message: {str(e)}")

async def cleanup_file(filename: str) -> None:
    """Robust file cleanup with retries"""
    if not filename or not os.path.exists(filename):
        return

    max_retries = 3
    for attempt in range(max_retries):
        try:
            os.remove(filename)
            logging.info(f"Cleaned up: {filename}")
            return
        except Exception as e:
            logging.warning(f"Cleanup attempt {attempt + 1} failed for {filename}: {str(e)}")
            if attempt < max_retries - 1:
                await asyncio.sleep(1)

    logging.error(f"Failed to cleanup file after {max_retries} attempts: {filename}")
