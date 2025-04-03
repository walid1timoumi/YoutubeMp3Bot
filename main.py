import asyncio
import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    Defaults
)
from config import BOT_TOKEN
from handlers.commands import start, help_command, cancel, settings
from handlers.messages import handle_message

async def post_init(application):
    """Post-initialization setup"""
    await application.bot.set_my_commands([
        ("start", "Start the bot"),
        ("help", "Show help guide"),
        ("cancel", "Cancel current operation"),
        ("settings", "Change bot settings")
    ])
    logging.info("Bot commands and setup completed")

def setup_handlers(application):
    """Register all handlers"""
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("settings", settings))
    
    # Message handler (MOST IMPORTANT)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(cancel, pattern="^cancel_"))
    application.add_handler(CallbackQueryHandler(settings, pattern="^(quality|format|main_menu)"))
async def error_handler(update: object, context):
    """Global error handler with proper typing"""
    logging.error("Exception occurred:", exc_info=context.error)
    
    if update and hasattr(update, 'effective_message'):
        await update.effective_message.reply_text(
            "⚠️ An error occurred. Our team has been notified.\n"
            "Please try again later.",
            parse_mode=None
        )

def main():
    """Configure and start the bot"""
    if not BOT_TOKEN:
        logging.critical("Missing BOT_TOKEN!")
        exit(1)
        
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .defaults(Defaults(parse_mode="Markdown"))
        .concurrent_updates(True)
        .build()
    )
    
    setup_handlers(application)
    application.add_error_handler(error_handler)
    
    logging.info("Starting bot...")
    print("Bot is running and waiting for messages...")  # Console confirmation
    application.run_polling(
        poll_interval=1.0,
        timeout=30,
        drop_pending_updates=True,
        allowed_updates=["message", "callback_query"]
    )

if __name__ == "__main__":
    main()