import asyncio
import threading
from flask import Flask, request, redirect
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes
)
import urllib.parse

BOT_TOKEN = "8067349631:AAEypPktMhYoL3aMH90u0d33R_U8tbU7WTg"
RAILWAY_BASE = "https://talented-stillness.up.railway.app/live"  # ✅ use your actual domain

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send PW .mp4 link, I'll convert for 1DM.")

async def handle_pw_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_link = update.message.text.strip()
    if not raw_link.startswith("http"):
        await update.message.reply_text("❌ Invalid link.")
        return

    try:
        encoded = urllib.parse.quote(raw_link, safe="")
        final_link = f"{RAILWAY_BASE}?q={encoded}&n=PW-Lecture"
        await update.message.reply_text(f"✅ 1DM Link:\n{final_link}")
    except Exception as e:
        await update.message.reply_text("❌ Failed.")
        print("Error:", e)

def start_telegram():
    async def run():
        bot = ApplicationBuilder().token(BOT_TOKEN).build()
        bot.add_handler(CommandHandler("start", start))
        bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_pw_link))
        await bot.run_polling()

    asyncio.run(run())

if __name__ == "__main__":
    threading.Thread(target=start_telegram).start()
    app.run(host="0.0.0.0", port=8080)
