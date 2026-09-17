import os
import logging
from datetime import datetime

import pytz
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TZ = pytz.timezone("Asia/Baghdad")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Team Report Bot is active.\n"
        "ڕۆبۆتی ڕاپۆرتی تیم چالاکە."
    )

async def collect_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    user = update.effective_user
    now = datetime.now(TZ)

    name = user.full_name if user else "Unknown"
    username = f"@{user.username}" if user and user.username else "-"

    if message.text:
        report_type = "TEXT"
        content = message.text

    elif message.voice:
        report_type = "VOICE"
        content = f"voice_file_id: {message.voice.file_id}"

    elif message.photo:
        report_type = "PHOTO"
        content = f"photo_file_id: {message.photo[-1].file_id}"

    elif message.video:
        report_type = "VIDEO"
        content = f"video_file_id: {message.video.file_id}"

    elif message.location:
        report_type = "LOCATION"
        content = (
            f"latitude: {message.location.latitude}, "
            f"longitude: {message.location.longitude}"
        )

    elif message.document:
        report_type = "DOCUMENT"
        content = f"document_file_id: {message.document.file_id}"

    else:
        report_type = "OTHER"
        content = "Unsupported message type"

    report = (
        f"\n--- TEAM REPORT ---\n"
        f"Time: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Name: {name}\n"
        f"Username: {username}\n"
        f"Type: {report_type}\n"
        f"Content: {content}\n"
    )

    logging.info(report)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(TZ)

    await update.message.reply_text(
        "✅ Team Report Bot is online.\n"
        f"🕒 {now.strftime('%Y-%m-%d %H:%M:%S')}"
    )

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured.")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))

    application.add_handler(
        MessageHandler(
            filters.TEXT
            | filters.VOICE
            | filters.PHOTO
            | filters.VIDEO
            | filters.LOCATION
            | filters.Document.ALL,
            collect_report,
        )
    )

    print("Team Report Bot started.")
    application.run_polling()

if __name__ == "__main__":
    main()
