import os
import sys
import psutil
from telegram import Update
from telegram.ext import ContextTypes
from services.system_monitor import SystemMonitor
from bot.middlewares import restricted

@restricted
async def system_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = SystemMonitor.get_system_stats()
    msg = (
        f"🖥 **System Status**\n"
        f"OS: `{stats['os']}`\n"
        f"CPU: `{stats['cpu_usage']}`\n"
        f"RAM: `{stats['ram_usage']}`\n"
        f"Disk: `{stats['disk_usage']}`\n"
        f"Python: `{stats['python']}`"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

@restricted
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 **RTMP Streamer Bot Help**\n\n"
        "📹 **Streaming**\n"
        "/stream - Start stream wizard\n"
        "/stop - Stop current stream\n"
        "/status - Show stream health\n\n"
        "📁 **Videos**\n"
        "/videos - List uploaded files\n"
        "Send any video file to upload it.\n\n"
        "📡 **RTMP**\n"
        "/addrtmp [name] [url] [key]\n"
        "/listrtmp - List destinations\n\n"
        "⚙️ **System**\n"
        "/system - Hardware stats\n"
        "/restart - Restart bot process"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

@restricted
async def restart_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Restarting bot...")
    os.execv(sys.executable, ['python3'] + sys.argv)
