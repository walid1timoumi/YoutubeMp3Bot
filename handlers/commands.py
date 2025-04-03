from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext
from typing import Optional

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for the /start command with enhanced welcome message"""
    welcome_msg = (
        "🎵 *YouTube to MP3 Bot*\n\n"
        "Send me any YouTube link to get high-quality MP3 audio!\n\n"
        "✨ *Features:*\n"
        "- Fast conversions\n"
        "- Multiple quality options\n"
        "- Cancel anytime\n\n"
        "Try it now by sending a YouTube link!"
    )
    
    await update.message.reply_text(
        welcome_msg,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❓ Help", callback_data="help"),
             InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
        ])
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Enhanced help command with detailed instructions"""
    help_text = (
        "🆘 *How to use this bot:*\n\n"
        "1. Send any YouTube link (video or playlist)\n"
        "2. Wait for processing (typically 30-90 seconds)\n"
        "3. Receive your MP3 file\n\n"
        "⚠️ *Limitations:*\n"
        "- Max 50MB file size (~15 min audio)\n"
        "- Some restricted videos may require cookies\n\n"
        "Commands:\n"
        "/start - Show welcome message\n"
        "/help - This message\n"
        "/cancel - Stop current conversion"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def cancel(update: Update, context: CallbackContext) -> Optional[bool]:
    """Improved cancellation handler with type hints"""
    if update.callback_query:
        query = update.callback_query
        if query.data.startswith("cancel_"):
            user_id = int(query.data.split("_")[1])
            if user_id == query.from_user.id:
                await query.answer("Conversion cancelled")
                await query.edit_message_text("❌ Conversion stopped")
                return True
    
    if update.message and context.user_data.get('active_download'):
        context.user_data['active_download'] = False
        await update.message.reply_text("✅ Stopped current conversion")
        return True
    
    await update.message.reply_text("⚠️ No active conversion to cancel")
    return False

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Settings menu with persistent options"""
    buttons = [
        [InlineKeyboardButton("🎧 Audio Quality", callback_data="quality")],
        [InlineKeyboardButton("📁 File Format", callback_data="format")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    await update.message.reply_text(
        "⚙️ *Bot Settings*",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode='Markdown'
    )