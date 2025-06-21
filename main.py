import asyncio
from flask import Flask, request, redirect
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes
)
import urllib.parse, threading, os

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE = os.getenv("API_BASE")  # Railway redirect URL

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ PW Redirect API is live."

@app.route("/live")
def redirector():
    raw = request.args.get("q")
    if not raw:
        return "❌ Missing 'q' param", 400
    return redirect(raw, 302)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send any PW video link (.mp4) and I’ll give a 1DM link!")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text.startswith("http"):
        await update.message.reply_text("❌ Invalid link.")
        return
    encoded = urllib.parse.quote(text, safe="")
    link = f"{API_BASE}?q={encoded}&n=PW"
    await update.message.reply_text(f"✅ 1DM Link:\n{link}")

async def start_bot():
    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling()
    await bot.updater.idle()

if __name__ == "__main__":
    threading.Thread(target=lambda: asyncio.run(start_bot()), daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
