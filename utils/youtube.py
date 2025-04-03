import re
import yt_dlp
import asyncio
import logging
from typing import Tuple, Optional

def is_valid_youtube_url(url: str) -> bool:
    """Improved URL validation that handles various formats"""
    patterns = [
        r'(https?://)?(www\.)?(youtube|youtu)\.(com|be)/(watch\?v=|embed/|v/|shorts/)?([^&=%\?]{11})',
        r'(https?://)?(www\.)?youtube\.com/playlist\?list=([^&=%\?]+)'
    ]
    return any(re.search(p, url) for p in patterns)

async def get_audio_url(url: str) -> Tuple[str, str]:
    """Robust audio extraction with multiple fallbacks"""
    ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': False,
    'extract_flat': False,
    'forceurl': True,
    'youtube_include_dash_manifest': False,
    'socket_timeout': 30,
    'extractor_args': {
        'youtube': {
            'skip': ['hls', 'dash', 'translated_subs'],
            'player_client': ['web']  # 🔥 Removed 'android' to avoid PO token issue
        }
    }
}


    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, url, download=False)
            
            if not info:
                raise Exception("No video information found - video may be private or removed")
            
            if 'url' not in info:
                # Try alternative extraction method
                if 'entries' in info:  # For playlists
                    entry = info['entries'][0]
                    if 'url' in entry:
                        return entry['url'], entry.get('title', 'YouTube Audio')
                raise Exception("No audio stream available - may be region restricted")
            
            return info['url'], info.get('title', 'YouTube Audio')

    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e).lower()
        if "private" in error_msg:
            raise Exception("🔒 Private video - cannot access")
        elif "age restricted" in error_msg:
            raise Exception("🔞 Age-restricted content - requires login")
        elif "unavailable" in error_msg:
            raise Exception("🌐 Video unavailable in your region")
        elif "copyright" in error_msg:
            raise Exception("⛔ Copyright-protected content")
        else:
            raise Exception(f"YouTube error: {str(e)[:200]}")
    except Exception as e:
        raise Exception(f"Processing error: {str(e)[:200]}")