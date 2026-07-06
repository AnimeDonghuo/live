from telegram import Update
from telegram.ext import ContextTypes
from database.mongo import db
from bot.middlewares import restricted

@restricted
async def add_rtmp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 3:
        return await update.message.reply_text("Usage: /addrtmp [Name] [URL] [Key]")
    
    name, url, key = args[0], args[1], args[2]
    full_url = f"{url}/{key}" if not url.endswith('/') else f"{url}{key}"
    
    await db.rtmp.update_one(
        {"name": name},
        {"$set": {"url": full_url, "base_url": url, "key": key}},
        upsert=True
    )
    await update.message.reply_text(f"✅ RTMP '{name}' saved.")

@restricted
async def list_rtmp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    servers = await db.rtmp.find().to_list(length=100)
    if not servers:
        return await update.message.reply_text("No RTMP servers configured.")
    
    msg = "📡 **RTMP Destinations:**\n\n"
    for s in servers:
        msg += f"• `{s['name']}`: {s['base_url']}\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

@restricted
async def delete_rtmp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /deletertmp [Name]")
    await db.rtmp.delete_one({"name": context.args[0]})
    await update.message.reply_text(f"Deleted RTMP {context.args[0]}")
