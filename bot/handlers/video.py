import os
import time
from telegram import Update
from telegram.ext import ContextTypes
from bot.config import Config
from database.mongo import db
from bot.middlewares import restricted
from utils.helpers import sanitize_filename, format_bytes

@restricted
async def handle_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video or update.message.document
    if not video.mime_type.startswith('video/'):
        return

    file_name = sanitize_filename(video.file_name or f"video_{int(time.time())}.mp4")
    file_path = os.path.join(Config.VIDEO_DIR, file_name)
    
    status_msg = await update.message.reply_text("📥 Downloading...")
    
    file = await context.bot.get_file(video.file_id)
    await file.download_to_drive(file_path)
    
    await db.videos.update_one(
        {"path": file_path},
        {"$set": {"name": file_name, "size": video.file_size, "added_at": time.time()}},
        upsert=True
    )
    
    await status_msg.edit_text(f"✅ Saved: `{file_name}` ({format_bytes(video.file_size)})", parse_mode="Markdown")

@restricted
async def list_videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    videos = await db.videos.find().to_list(length=100)
    if not videos: return await update.message.reply_text("No videos uploaded.")
    
    msg = "📂 **Available Videos:**\n\n"
    for v in videos:
        msg += f"• `{v['name']}` ({format_bytes(v['size'])})\n"
    await update.message.reply_text(msg, parse_mode="Markdown")
