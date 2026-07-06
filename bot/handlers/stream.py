from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.ffmpeg_manager import stream_manager
from database.mongo import db
import humanize
import datetime

async def stream_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Step 1: Select Video
    videos = await db.videos.find().to_list(length=50)
    if not videos:
        await update.message.reply_text("No videos found. Upload one first.")
        return

    keyboard = [[InlineKeyboardButton(v['name'], callback_data=f"sel_vid_{v['_id']}")] for v in videos]
    await update.message.reply_text("Select a video to stream:", reply_markup=InlineKeyboardMarkup(keyboard))

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await stream_manager.stop_stream()
    await update.message.reply_text("🛑 Stream stopped.")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = stream_manager.get_status()
    if not status:
        await update.message.reply_text("Status: ⚪ Stopped")
        return

    uptime = str(datetime.timedelta(seconds=int(status['uptime'])))
    msg = (
        f"🟢 **Streaming: Running**\n"
        f"📹 Video: `{status['video']}`\n"
        f"🔗 RTMP: `{status['rtmp']}`\n"
        f"⏱ Uptime: `{uptime}`\n"
        f"💻 CPU: `{status['cpu']}%` | RAM: `{status['mem']:.1f}%`\n"
        f"🆔 PID: `{status['pid']}`"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")
