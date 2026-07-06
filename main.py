import sys
import asyncio
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from bot.config import Config
from utils.logger import setup_logger
from services.system_monitor import SystemMonitor
from bot.handlers import admin, rtmp, stream, video
from bot.middlewares import owner_only

async def main():
    # Setup Logger
    logger = setup_logger()
    
    # Pre-flight checks
    logger.info("Running pre-flight checks...")
    errors = await SystemMonitor.run_preflight_checks()
    if errors:
        for err in errors:
            logger.critical(f"STARTUP ERROR: {err}")
        sys.exit(1)
    
    # Init Bot
    app = ApplicationBuilder().token(Config.BOT_TOKEN).build()
    
    # Add Handlers
    app.add_handler(CommandHandler("start", admin.help_command))
    app.add_handler(CommandHandler("help", admin.help_command))
    app.add_handler(CommandHandler("system", admin.system_command))
    
    app.add_handler(CommandHandler("addrtmp", rtmp.add_rtmp))
    app.add_handler(CommandHandler("listrtmp", rtmp.list_rtmp))
    
    app.add_handler(CommandHandler("stream", stream.stream_command))
    app.add_handler(CommandHandler("stop", stream.stop_command))
    app.add_handler(CommandHandler("status", stream.status_command))
    
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, video.handle_upload))
    
    logger.info("Bot started successfully.")
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
