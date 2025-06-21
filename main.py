import asyncio
from flask import Flask, request, redirect
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
import urllib.parse
import threading

BOT_TOKEN = "8067349631:AAEypPktMhYoL3aMH90u0d33R_U8tbU7WTg"
RAILWAY_BASE = "https://talented-stillness.up.railway.app/live"

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ PW Redirect API is Live"

@app.route("/live")
def redirector():
    raw_url = request.args.get("q")
    if not raw_url:
        return "❌ Missing 'q' parameter", 400
    return redirect(raw_url, code=302)

# Telegram bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send any PW video link and I’ll return a 1DM link.")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw = update.message.text.strip()
    if not raw.startswith("http"):
        await update.message.reply_text("❌ Invalid URL.")
        return
    encoded = urllib.parse.quote(raw, safe="")
    final = f"{RAILWAY_BASE}?q={encoded}&n=PW"
    await update.message.reply_text(f"✅ 1DM Link:\n{final}")

# Launch bot inside asyncio task
def run_bot():
    async def main():
        bot = ApplicationBuilder().token(BOT_TOKEN).build()
        bot.add_handler(CommandHandler("start", start))
        bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
        await bot.initialize()
        await bot.start()
        await bot.updater.start_polling()
        await bot.updater.idle()
    asyncio.create_task(main())

# Flask entrypoint
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app.run(host="0.0.0.0", port=8080)
